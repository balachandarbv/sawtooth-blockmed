import hashlib
import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import processor.common.helper as helper
from processor.workflow.payload import HealthCarePayload
from processor.workflow.state import HealthCareState
from processor.common.protobuf.payload_pb2 import Claim

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class HealthCareTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return helper.TP_FAMILYNAME

    @property
    def family_versions(self):
        return [helper.TP_VERSION]

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        try:

            _display("i'm inside handler _display")
            print("i'm inside handler print")

            header = transaction.header
            signer = header.signer_public_key
            healthcare_payload = HealthCarePayload(payload=transaction.payload)
            healthcare_state = HealthCareState(context)

            if healthcare_payload.is_create_clinic():
                clinic = healthcare_payload.create_clinic()

                cl = healthcare_state.get_clinic(signer)
                if cl is not None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic already exists: ' + clinic.name)

                healthcare_state.create_clinic(clinic)
            elif healthcare_payload.is_create_doctor():
                doctor = healthcare_payload.create_doctor()

                do = healthcare_state.get_doctor(doctor.doctor_key)
                LOGGER.warning("Doctor Key: " + str(do))
                if do is not None:
                    raise InvalidTransaction(
                        'Invalid action: Doctor already exists: ' + doctor.name)

                healthcare_state.create_doctor(doctor)

            elif healthcare_payload.is_create_party():
                party = healthcare_payload.create_party()

                LOGGER.warning("Party Key: " + str(party.public_key))

                do = healthcare_state.get_party(party.public_key)
                LOGGER.warning("Party Key: " + str(do))
                if do is not None:
                    raise InvalidTransaction(
                        'Invalid action: Doctor already exists: ' + party.name)

                healthcare_state.create_party(party)

            elif healthcare_payload.is_create_patient():
                patient = healthcare_payload.create_patient()
                pat = healthcare_state.get_patient(patient.record_id)
                if pat is not None:
                    raise InvalidTransaction(
                        'Invalid action: Patient already exists: ' + patient.name)

                healthcare_state.create_patient(patient)


            elif healthcare_payload.is_create_evaluation():
                evaluation = healthcare_payload.create_evaluation()
                eva = healthcare_state.get_evaluation(evaluation.record_id)
                if eva is not None:
                    raise InvalidTransaction(
                        'Invalid action: Patient already exists: ' + evaluation.record_id)

                healthcare_state.create_evaluation(evaluation)

            elif healthcare_payload.is_create_evaluation_record():
                evaluation_record = healthcare_payload.create_evaluation_record()
                eva = healthcare_state.create_evaluation_record(evaluation_record)
                if eva is not None:
                    raise InvalidTransaction(
                        'Invalid action: Patient already exists: ' + evaluation_record.record_id)

                healthcare_state.create_evaluation_record(evaluation_record)

            elif healthcare_payload.is_create_consent():
                consent_record = healthcare_payload.create_doctor_patient_consent()
                cons = healthcare_state.create_consent(consent_record)
                if cons is not None:
                    raise InvalidTransaction(
                        'Invalid action: Patient already exists: ' + cons.consent_id)

                healthcare_state.create_consent(consent_record)


            elif healthcare_payload.is_update_evaluation_record():

                evaluation_record = healthcare_payload.update_evaluation_record()
                evaluation_record_org = healthcare_state.get_evaluation_record(evaluation_record.record_id)
                if evaluation_record_org is None:
                    raise InvalidTransaction(
                        'Invalid action: Evaluation record, does not exist: ' + evaluation_record.record_id)
                if evaluation_record.records!=None:
                    evaluation_record_org.records.extend(evaluation_record.records)
                if evaluation_record.consent != None:
                    for item in evaluation_record.consent:
                        evaluation_record_org.consent[item]=evaluation_record.consent[item]

                healthcare_state.update_evaluation_record(evaluation_record_org)

            elif healthcare_payload.is_create_lab():
                lab = healthcare_payload.create_lab()

                lb = healthcare_state.get_lab(signer)
                if lb is not None:
                    raise InvalidTransaction(
                        'Invalid action: Lab already exists: ' + lb.name)

                healthcare_state.create_lab(lab)
            elif healthcare_payload.is_create_claim():

                claim = healthcare_payload.create_claim()
                cl = healthcare_state.get_claim2(claim.id)
                if cl is not None:
                    raise InvalidTransaction(
                        'Invalid action: Claim already exist: ' + cl.id)

                healthcare_state.create_claim(claim)
            elif healthcare_payload.is_close_claim():

                claim = healthcare_payload.close_claim()
                original_claim = healthcare_state.get_claim2(claim.id)
                if original_claim is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + claim.id)
                if original_claim.state == Claim.CLOSED:
                    raise InvalidTransaction(
                        'Invalid action: Claim already closed: ' + claim.id)
                original_claim.provided_service = claim.provided_service
                original_claim.state = Claim.CLOSED
                healthcare_state.close_claim(original_claim)
            elif healthcare_payload.is_update_claim():

                claim = healthcare_payload.update_claim()
                original_claim = healthcare_state.get_claim2(claim.id)
                if original_claim is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + claim.id)
                if original_claim.state == Claim.CLOSED:
                    raise InvalidTransaction(
                        'Invalid action: Can not update closed claim: ' + claim.id)
                original_claim.provided_service = claim.provided_service
                # original_claim.state = Claim.CLOSED
                healthcare_state.update_claim(original_claim)
            elif healthcare_payload.is_assign_doctor():
                assign = healthcare_payload.assign_doctor()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(assign.claim_id, assign.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + assign.claim_id + '; clinic: ' + clinic.public_key)

                healthcare_state.assign_doctor(assign.claim_id, assign.clinic_pkey, assign.description,
                                               assign.event_time)
            elif healthcare_payload.is_first_visit():
                visit = healthcare_payload.first_visit()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(visit.claim_id, visit.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + visit.claim_id)

                healthcare_state.first_visit(visit.claim_id, visit.clinic_pkey,
                                             visit.description, visit.event_time)
            elif healthcare_payload.is_pass_tests():
                tests = healthcare_payload.pass_tests()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(tests.claim_id, tests.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + tests.claim_id)

                healthcare_state.pass_tests(tests.claim_id, tests.clinic_pkey, tests.description, tests.event_time)
            elif healthcare_payload.is_attend_procedures():
                procedures = healthcare_payload.attend_procedures()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(procedures.claim_id, procedures.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + procedures.claim_id)

                healthcare_state.attend_procedures(procedures.claim_id, procedures.clinic_pkey, procedures.description,
                                                   procedures.event_time)
            elif healthcare_payload.is_eat_pills():
                pills = healthcare_payload.eat_pills()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(pills.claim_id, pills.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + pills.claim_id)

                healthcare_state.eat_pills(pills.claim_id, pills.clinic_pkey, pills.description,
                                           pills.event_time)
            elif healthcare_payload.is_next_visit():
                examination = healthcare_payload.next_visit()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(examination.claim_id, examination.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + examination.claim_id)

                healthcare_state.next_visit(examination.claim_id, examination.clinic_pkey,
                                            examination.description,
                                            examination.event_time)
            elif healthcare_payload.is_lab_test():
                lab_test = healthcare_payload.lab_test()

                # clinic = healthcare_state.get_clinic(signer)
                # if clinic is None:
                #     raise InvalidTransaction(
                #         'Invalid action: Clinic does not exist: ' + signer)

                # healthcare_state.add_lab_test(signer, lab_test.height, lab_test.weight, lab_test.gender,
                #                               lab_test.a_g_ratio, lab_test.albumin, lab_test.alkaline_phosphatase,
                #                               lab_test.appearance, lab_test.bilirubin, lab_test.casts,
                #                               lab_test.color, lab_test.event_time)
                healthcare_state.add_lab_test(lab_test)
            elif healthcare_payload.is_pulse():
                pulse = healthcare_payload.pulse()

                # patient = healthcare_state.get_patient(signer)
                # if patient is None:
                #     raise InvalidTransaction(
                #         'Invalid action: Patient does not exist: ' + signer)

                healthcare_state.add_pulse(pulse)
            else:
                raise InvalidTransaction('Unhandled action: {}'.format(healthcare_payload.transaction_type()))
        except Exception as e:
            print("Error: {}".format(e))
            logging.exception(e)
            raise InvalidTransaction(repr(e))


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
