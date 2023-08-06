
from pandas._testing import assert_series_equal
from unittest import TestCase
from .test_fhir_bundle import socket_data
from .helpers import AiConvertionHelper


class TestAiInputConverter(TestCase):
    TEST_BUNDLE = socket_data
    TEST_HELPER = AiConvertionHelper

    # def test_conversion(self):
    #     ai_converter = converter.FHIRConverter()
    #
    #     claim_bundle_input_models, _ = ai_converter.bundle_ai_input(self.TEST_BUNDLE)
    #     self.assertEqual(len([claim for claim, _ in claim_bundle_input_models]), 1)  # input_bundle generated for single claim
    #
    #     generated_input = []
    #     for _, claim_input_models in claim_bundle_input_models:
    #         for next_input_model in claim_input_models:
    #             generated_input.append(next_input_model.to_representation())
    #
    #     self.assertEqual(len(generated_input), self.TEST_HELPER.EXPECTED_NUMBER_OF_ENTRIES)
    #     self.__asert_items(generated_input)
    #     self.__asert_services(generated_input)
    #     self.__asert_healthcare_service(generated_input)
    #     self.__asert_patient(generated_input)
    #     self.__asert_item_independent_claim_fields(generated_input)
    #
    #     assert_frame_equal(generated_input[0], self.TEST_HELPER.EXPECTED_DATAFRAME_ITEM)
    #     assert_frame_equal(generated_input[1], self.TEST_HELPER.EXPECTED_DATAFRAME_SERVICE)

    def __asert_items(self, generated_input):
        items = [frame for frame in generated_input if 'Medication' in frame.columns]

        item_frame = items[0]
        item_data_column = item_frame['Medication']
        item_identifier = item_data_column[0]
        item_unit_price = item_data_column[1]
        item_frequency = item_data_column[2]
        item_use_context = item_data_column[3]
        item_provision_level = item_data_column[4]
        item_provision_type = item_data_column[5]

        expected_number_of_items = self.TEST_HELPER.EXPECTED_NUMBER_OF_ITEM_ENTRIES
        expected_item = self.TEST_HELPER.EXPECTED_ITEM_ENTRY
        self.assertEqual(len(items), expected_number_of_items)
        self.assertEqual(item_identifier, expected_item['identifier'])
        self.assertEqual(item_unit_price, expected_item['unitPrice'])
        self.assertEqual(item_frequency, expected_item['frequency'])
        self.assertEqual(item_use_context, expected_item['useContext'])
        self.assertEqual(item_provision_level, expected_item['item_level'])
        self.assertEqual(item_provision_type, expected_item['type'])

    def __asert_services(self, generated_input):
        services = [frame for frame in generated_input if 'ActivityDefinition' in frame.columns]

        service_frame = services[0]
        service_data_column = service_frame['ActivityDefinition']
        claim_data_column = service_frame['Claim']
        service_identifier = service_data_column[0]
        service_unit_price = service_data_column[1]
        service_frequency = service_data_column[2]
        service_use_context = service_data_column[3]
        item_provision_level = service_data_column[4]
        service_provision_type = service_data_column[5]

        expected_number_of_services = self.TEST_HELPER.EXPECTED_NUMBER_OF_SERVICE_ENTRIES
        expected_service = self.TEST_HELPER.EXPECTED_SERVICE_ENTRY
        self.assertEqual(len(services), expected_number_of_services)
        self.assertEqual(service_identifier, expected_service['identifier'])
        self.assertEqual(service_unit_price, expected_service['unitPrice'])
        self.assertEqual(service_frequency, expected_service['frequency'])
        self.assertEqual(service_use_context, expected_service['useContext'])
        self.assertEqual(item_provision_level, expected_service['item_level'])
        self.assertEqual(service_provision_type, expected_service['type'])

        service_claim_quantity = claim_data_column[5]
        service_claim_unit_price = claim_data_column[6]
        expected_claim = self.TEST_HELPER.EXPECTED_CLAIM_ENTRY_FOR_SERVICE

        self.assertEqual(service_claim_unit_price, expected_claim['item.unitPrice'])
        self.assertEqual(service_claim_quantity, expected_claim['item.quantity'])

    def __asert_healthcare_service(self, generated_input):
        # Healthcare for all claim entries should be the same
        assert_series_equal(generated_input[0]['HealthcareService'], generated_input[1]['HealthcareService'])

        healthcare_column = generated_input[0]['HealthcareService']
        healthcare_identifier = healthcare_column[0]
        healthcare_location = healthcare_column[1]
        healthcare_category = healthcare_column[2]
        healthcare_type = healthcare_column[3]

        expected_healthcare = self.TEST_HELPER.EXPECTED_HEALTHCARE_ENTRY

        self.assertEqual(healthcare_identifier, expected_healthcare['identifier'])
        self.assertEqual(healthcare_location, expected_healthcare['location'])
        self.assertEqual(healthcare_category, expected_healthcare['category'])
        self.assertEqual(healthcare_type, expected_healthcare['type'])

    def __asert_patient(self, generated_input):
        assert_series_equal(generated_input[0]['Patient'], generated_input[1]['Patient'])

        patient_frame = generated_input[0]['Patient']
        patient_identifier = patient_frame[0]
        patient_birthDate = patient_frame[1]
        patient_gender = patient_frame[2]
        patient_isHead = patient_frame[3]
        patient_povertyStatus = patient_frame[4]
        patient_locationCode = patient_frame[5]
        patient_group = patient_frame[6]

        expected_patient = self.TEST_HELPER.EXPECTED_PATIENT_ENTRY

        self.assertEqual(patient_identifier, expected_patient['identifier'])
        self.assertEqual(patient_birthDate, expected_patient['birthDate'])
        self.assertEqual(patient_gender, expected_patient['gender'])
        self.assertEqual(patient_isHead, expected_patient['isHead'])
        self.assertEqual(patient_povertyStatus, expected_patient['povertyStatus'])
        self.assertEqual(patient_locationCode, expected_patient['locationCode'])
        self.assertEqual(patient_group, expected_patient['group'])

    def __asert_item_independent_claim_fields(self, generated_input):
        non_mutable_claim_fields = [0, 1, 2, 3, 4, 7, 8, 9]
        # Compare fields not related to item
        assert_series_equal(
            generated_input[0]['Claim'].iloc[non_mutable_claim_fields],
            generated_input[1]['Claim'].iloc[non_mutable_claim_fields]
        )
        claim_frame = generated_input[0]['Claim']
        claim_identifier = claim_frame[0]
        claim_billable_period_from = claim_frame[1]
        claim_billable_period_to = claim_frame[2]
        claim_created = claim_frame[3]
        claim_type = claim_frame[4]
        claim_diagnosis_0 = claim_frame[7]
        claim_diagnosis_1 = claim_frame[8]
        claim_enterer = claim_frame[9]

        expected_claim = self.TEST_HELPER.EXPECTED_NON_MUTABLE_CLAIM_ENTRY_FIELDS
        self.assertEqual(claim_identifier, expected_claim['identifier'])
        self.assertEqual(claim_billable_period_from, expected_claim['billablePeriod_from'])
        self.assertEqual(claim_billable_period_to, expected_claim['billablePeriod_to'])
        self.assertEqual(claim_created, expected_claim['created'])
        self.assertEqual(claim_type, expected_claim['type'])
        self.assertEqual(claim_diagnosis_0, expected_claim['diagnosis.diagnosisReference_0'])
        self.assertEqual(claim_diagnosis_1, expected_claim['diagnosis.diagnosisReference_1'])
        self.assertEqual(claim_enterer, expected_claim['enterer'])
