import logging

from rest_framework.generics import get_object_or_404

from api_fhir_r4.converters import ClaimResponseConverter
from api_fhir_r4.serializers import ClaimSerializer
from claim.models import Claim
from claim_ai.models import ClaimBundleEvaluation
from claim_ai.rest_api.claim_evaluation.claim_bundle_evaluation_manager import ClaimBundleEvaluationManager
from claim_ai.rest_api.claim_evaluation.serializer_data_handlers import ResponseHandler, RequestToInternalValueHandler

logger = logging.getLogger(__name__)


class ClaimBundleEvaluationSerializer(ClaimSerializer):
    """
    Uses FHIR Serializer to create claims and claim bundles. Submitted claims are evaluated using AI after
    submission using celery task. While retrieving resource from database instead of
    FHIR Claim it uses claim bundle evaluation result and returns AI CLaimResponse bundle with all claims evaluated
    in scope of this bundle.
    """

    def __init__(self, *args, **kwargs):
        self._wait = kwargs.pop('wait')
        super().__init__(*args, **kwargs)
        self.request_handler = RequestToInternalValueHandler(self.fhirConverter, self.get_audit_user_id())
        self.response_handler = ResponseHandler()
        user = self.context.get("request").user
        self.evaluation_bundle_manager = ClaimBundleEvaluationManager(user)

    def to_representation(self, obj):
        return self.response_handler.to_representation(obj)

    def to_internal_value(self, data):
        return self.request_handler.to_internal_value(data)

    def create(self, validated_data):
        from_contained = self._create_or_update_contained(self.initial_data)
        imis_claims = self._imis_claims_from_validated_data(validated_data, from_contained)
        evaluation_bundle_hash = validated_data.get('bundle_id')
        evaluation_data = self.evaluation_bundle_manager\
            .create_idle_evaluation_bundle(imis_claims, evaluation_bundle_hash)
        evaluation_info = self._add_claims_for_evaluation_query(evaluation_data)
        return evaluation_info

    def create_claim_response(self, claim_code):
        claim = get_object_or_404(Claim, code=claim_code, validity_to=None)
        return ClaimResponseConverter.to_fhir_obj(claim)

    def _imis_claims_from_validated_data(self, validated_data, contained):
        out = []
        for claim in validated_data['claims']:
            existing_claim = Claim.objects.filter(uuid=claim['uuid']).first()
            if existing_claim:
                # TODO: Implement overriding data
                logger.warning(
                    F"Claim {claim['uuid']} was already sent for evaluation. "
                    F"It's definition will not be updated.")
                out.append(existing_claim)
            else:
                out.append(self._submit_claim(claim, contained))
        return out

    def _create_or_update_contained(self, initial_data):
        if initial_data['resourceType'] == 'Bundle':
            unique_contained = self._unique_contained_resources(initial_data)
            initial_data['contained'] = unique_contained
        result = self._create_contained_from_claim(initial_data)
        return result

    def __cast_to_fhir_with_contained(self, obj):
        fhir_obj = self.fhirConverter.to_fhir_obj(obj, self._reference_type)
        self.remove_attachment_data(fhir_obj)
        self._add_contained_references(fhir_obj)

        fhir_dict = fhir_obj.dict()
        fhir_dict['contained'] = self._create_contained_obj_dict(obj)
        return fhir_dict

    def _unique_contained_resources(self, bundle):
        # If given resource is defined multiple times in scope of single request it's saved only once.
        unique_contained_by_id = {}
        for claim in bundle['entry']:
            for contained_source in claim['resource'].get('contained', []):
                unique_key = F"{contained_source['resourceType']}_{contained_source['id']}"
                unique_contained_by_id[unique_key] = contained_source
        return unique_contained_by_id.values()

    def _create_contained_from_claim(self, fhir_claim_dict: dict):
        result = {}
        for resource in self._contained_definitions.get_contained().values():
            name = resource.alias
            result[name] = resource.create_or_update_from_contained(fhir_claim_dict)
        return result

    def _submit_claim(self, claim, contained):
        # If there was predefined UUID use it instead of new one
        uuid = claim.get('uuid') or None
        new_claim = self._create_claim_from_validated_data(claim, contained)
        if uuid:
            new_claim.uuid = uuid
            new_claim.save()
        return new_claim

    def _add_claims_for_evaluation_query(self, evaluation_data: ClaimBundleEvaluation):
        if not self._wait:
            self.evaluation_bundle_manager.query_claims_for_evaluation(evaluation_data)
            return evaluation_data
        else:
            evaluation = self.evaluation_bundle_manager.evaluate_bundle(evaluation_data)
            return evaluation
