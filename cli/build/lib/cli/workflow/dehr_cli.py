import argparse
import getpass
import logging
import os
import sys
import traceback

import pkg_resources
from colorlog import ColoredFormatter
from sawtooth_signing import create_context #, CryptoFactory

from cli.common.helper import DISTRIBUTION_NAME, DEFAULT_URL
from cli.common.exceptions import HealthCareException
from cli.workflow.dehr_client import HealthCareClient


def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)

    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)

    return clog


def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))


def add_create_clinic_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'create_clinic',
        help='Creates new clinic',
        description='Generates new private key and registers new clinic in blockchain',
        parents=[parent_parser])

    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='specify clinic name')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    # parser.add_argument(
    #     '--username',
    #     type=str,
    #     help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    # parser.add_argument(
    #     '--auth-user',
    #     type=str,
    #     help='specify username for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--auth-password',
    #     type=str,
    #     help='specify password for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--disable-client-validation',
    #     action='store_true',
    #     default=False,
    #     help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for game to commit')


def add_create_doctor_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'create_doctor',
        help='Creates new doctor',
        description='Sends a transaction to create an doctor with the '
                    'identifier <name>. This transaction will fail if the specified '
                    'doctor already exists.',
        parents=[parent_parser])

    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='specify doctor name')

    parser.add_argument(
        '--surname',
        type=str,
        required=True,
        help='specify doctor surname')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    # parser.add_argument(
    #     '--username',
    #     type=str,
    #     help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    # parser.add_argument(
    #     '--auth-user',
    #     type=str,
    #     help='specify username for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--auth-password',
    #     type=str,
    #     help='specify password for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--disable-client-validation',
    #     action='store_true',
    #     default=False,
    #     help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for game to commit')


def add_create_patient_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'create_patient',
        help='Creates new patient',
        description='Sends a transaction to create an patient with the '
                    'identifier <name>. This transaction will fail if the specified '
                    'patient already exists.',
        parents=[parent_parser])

    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='specify patient name')

    parser.add_argument(
        '--surname',
        type=str,
        required=True,
        help='specify patient surname')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    # parser.add_argument(
    #     '--username',
    #     type=str,
    #     help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    # parser.add_argument(
    #     '--auth-user',
    #     type=str,
    #     help='specify username for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--auth-password',
    #     type=str,
    #     help='specify password for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--disable-client-validation',
    #     action='store_true',
    #     default=False,
    #     help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for game to commit')


def add_lab_test_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'add_lab_test',
        help='Adds a lab test',
        description='Sends a transaction to create a lab test',
        parents=[parent_parser])

    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='specify clinic name')

    parser.add_argument(
        '--height',
        type=str,
        required=True,
        default='0',
        help='specify height')

    parser.add_argument(
        '--weight',
        type=str,
        required=True,
        default='0',
        help='specify weight')

    parser.add_argument(
        '--gender',
        type=str,
        required=True,
        default='male',
        help='specify male or female')

    parser.add_argument(
        '--a_g_ratio',
        type=str,
        required=True,
        default='0',
        help='specify a/g ratio')

    parser.add_argument(
        '--albumin',
        type=str,
        required=True,
        default='0',
        help='specify albumin')

    parser.add_argument(
        '--alkaline_phosphatase',
        type=str,
        required=True,
        default='0',
        help='specify alkaline phosphatase')

    parser.add_argument(
        '--appearance',
        type=str,
        required=True,
        default='0',
        help='specify appearance')

    parser.add_argument(
        '--bilirubin',
        type=str,
        required=True,
        default='0',
        help='specify bilirubin')

    parser.add_argument(
        '--casts',
        type=str,
        required=True,
        default='0',
        help='specify casts')

    parser.add_argument(
        '--color',
        type=str,
        required=True,
        default='n/a',
        help='specify color')

    # parser.add_argume
    #     '--username',
    #     type=str,
    #     help="identify name of user's private key file")

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    # parser.add_argument(
    #     '--auth-user',
    #     type=str,
    #     help='specify username for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--auth-password',
    #     type=str,
    #     help='specify password for authentication if REST API '
    #          'is using Basic Auth')
    #
    # parser.add_argument(
    #     '--disable-client-validation',
    #     action='store_true',
    #     default=False,
    #     help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for game to commit')


def add_pulse_parser(subparsers, parent_parser):

    parser = subparsers.add_parser(
        'add_pulse',
        help='Adds a pulse',
        description='Sends a transaction to create a pulse',
        parents=[parent_parser])

    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='specify patient name')

    parser.add_argument(
        '--pulse',
        type=str,
        required=True,
        help='specify pulse value')

    parser.add_argument(
        '--timestamp',
        type=str,
        required=True,
        default='0',
        help='specify timestamp')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for game to commit')
#
# def add_create_claim_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'create_claim',
#         help='Add new claim',
#         description='Sends a transaction to add new claim.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim id in clinics\'s network')
#
#     parser.add_argument(
#         '--patient_pkey',
#         type=str,
#         required=True,
#         help='specify patient pkey')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')
#
#
# def add_assign_doctor_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'assign_doctor',
#         help='Assign doctor',
#         description='Sends a transaction to assign doctor.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id in clinic\'s network')
#
#     parser.add_argument(
#         '--doctor_pkey',
#         type=str,
#         required=True,
#         help='specify doctor pkey in clinic\'s network')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')
#
#
# def add_first_visit_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'first_visit',
#         help='Complete first visit',
#         description='Sends a transaction to first visit.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id')
#
#     parser.add_argument(
#         '--doctor_pkey',
#         type=str,
#         required=True,
#         help='specify doctor pkey')
#
#     parser.add_argument(
#         '--description',
#         type=str,
#         required=True,
#         help='specify description')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')
#
#
# def add_pass_tests_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'pass_tests',
#         help='Pass tests',
#         description='Sends a transaction to pass tests.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id')
#
#     parser.add_argument(
#         '--description',
#         type=str,
#         required=True,
#         help='specify description')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')
#
#
# def add_attend_procedures_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'attend_procedures',
#         help='Attend procedures',
#         description='Sends a transaction to attend procedures.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id')
#
#     parser.add_argument(
#         '--description',
#         type=str,
#         required=True,
#         help='specify description')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')
#
#
# def add_eat_pills_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'eat_pills',
#         help='Eat pills',
#         description='Sends a transaction to eat pills.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--description',
#         type=str,
#         required=True,
#         help='specify description')
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')
#
#
# def add_next_visit_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'next_visit',
#         help='Complete next examination',
#         description='Sends a transaction to complete next examination.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--description',
#         type=str,
#         required=True,
#         help='specify description')
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id')
#
#     parser.add_argument(
#         '--doctor_pkey',
#         type=str,
#         required=True,
#         help='specify doctor hex')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--disable-client-validation',
#         action='store_true',
#         default=False,
#         help='disable client validation')
#
#     parser.add_argument(
#         '--wait',
#         nargs='?',
#         const=sys.maxsize,
#         type=int,
#         help='set time, in seconds, to wait for game to commit')


def add_list_clinics_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'list_clinics',
        help='Displays information for all clinics',
        description='Displays information for all clinics in state.',
        parents=[parent_parser])

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    # parser.add_argument(
    #     '--username',
    #     type=str,
    #     help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")


def add_list_doctors_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'list_doctors',
        help='Displays information for all doctors',
        description='Displays information for all doctors in state.',
        parents=[parent_parser])

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")


def add_list_patients_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'list_patients',
        help='Displays information for all patients',
        description='Displays information for all patients in state.',
        parents=[parent_parser])

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")


def add_list_lab_test_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'list_lab_test',
        help='Displays information for all lab test',
        description='Displays information for all lab test in state.',
        parents=[parent_parser])

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")


def add_list_pulse_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'list_pulse',
        help='Displays information for all pulse items',
        description='Displays information for all pulse items in state.',
        parents=[parent_parser])

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

# def add_list_claim_details_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'list_claim_details',
#         help='Displays information for the claim',
#         description='Displays information for the claim in state.',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--claim_id',
#         type=str,
#         required=True,
#         help='specify claim_id')
#
#     parser.add_argument(
#         '--clinic_pkey',
#         type=str,
#         required=True,
#         help='specify clinic pkey')
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')
#
#
# def add_list_claims_parser(subparsers, parent_parser):
#     parser = subparsers.add_parser(
#         'list_claims',
#         help='Displays information for all claims',
#         description='Displays information for all claims in state',
#         parents=[parent_parser])
#
#     parser.add_argument(
#         '--url',
#         type=str,
#         help='specify URL of REST API')
#
#     parser.add_argument(
#         '--username',
#         type=str,
#         help="identify name of user's private key file")
#
#     parser.add_argument(
#         '--key-dir',
#         type=str,
#         help="identify directory of user's private key file")
#
#     parser.add_argument(
#         '--auth-user',
#         type=str,
#         help='specify username for authentication if REST API '
#              'is using Basic Auth')
#
#     parser.add_argument(
#         '--auth-password',
#         type=str,
#         help='specify password for authentication if REST API '
#              'is using Basic Auth')


def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output')

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}').format(version),
        help='display version information')

    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to healthcare.',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    # add_assign_doctor_parser(subparsers, parent_parser)
    # add_first_visit_parser(subparsers, parent_parser)
    # add_pass_tests_parser(subparsers, parent_parser)
    # add_attend_procedures_parser(subparsers, parent_parser)
    # add_eat_pills_parser(subparsers, parent_parser)
    # add_next_visit_parser(subparsers, parent_parser)
    # add_create_claim_parser(subparsers, parent_parser)
    add_create_clinic_parser(subparsers, parent_parser)
    add_create_doctor_parser(subparsers, parent_parser)
    add_create_patient_parser(subparsers, parent_parser)
    add_lab_test_parser(subparsers, parent_parser)
    add_pulse_parser(subparsers, parent_parser)
    # add_list_claims_parser(subparsers, parent_parser)
    add_list_clinics_parser(subparsers, parent_parser)
    add_list_doctors_parser(subparsers, parent_parser)
    add_list_patients_parser(subparsers, parent_parser)
    add_list_lab_test_parser(subparsers, parent_parser)
    add_list_pulse_parser(subparsers, parent_parser)
    # add_list_claim_details_parser(subparsers, parent_parser)
    return parser


def do_list_clinics(args):
    url = _get_url(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=None)

    clinic_list = client.list_clinics()

    if clinic_list is not None:
        fmt = "%-15s %-15s %-15s"
        print(fmt % ('HEX', 'NAME', 'PUBLIC_KEY'))
        for key, value in clinic_list.items():
            print(fmt % (key, value.name, value.public_key))
    else:
        raise HealthCareException("Could not retrieve clinic listing.")


def do_list_doctors(args):
    url = _get_url(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=None)

    doctors_list = client.list_doctors()

    if doctors_list is not None:
        fmt = "%-15s %-15s %-15s"
        print(fmt % ('NAME', 'SURNAME', 'PUBLIC_KEY'))
        for doctor in doctors_list:
            print(fmt % (doctor.name, doctor.surname, doctor.public_key))
    else:
        raise HealthCareException("Could not retrieve doctors listing.")


def do_list_patients(args):
    url = _get_url(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=None)

    patient_list = client.list_patients()

    if patient_list is not None:
        fmt = "%-15s %-15s %-15s %-15s"
        print(fmt % ('PATIENT HEX', 'NAME', 'SURNAME', 'PUBLIC_KEY'))
        for key, value in patient_list.items():
            print(fmt % (key, value.name, value.surname, value.public_key))
    else:
        raise HealthCareException("Could not retrieve patient listing.")


def do_list_lab_test(args):
    url = _get_url(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=None)

    lab_test_list = client.list_lab_test()

    if lab_test_list is not None:
        fmt = "%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s"
        print(fmt % ('CLINIC HEX', 'HEIGHT', 'WEIGHT', 'GENDER', 'A/G RATIO', 'ALBUMIN', 'ALKALINE PHOSPHATASE',
                     'APPEARANCE', 'BILIRUBIN', 'CASTS', 'COLOR'))
        for key, value in lab_test_list.items():
            print(fmt % (key, value.height, value.weight, value.gender, value.a_g_ratio, value.albumin,
                         value.alkaline_phosphatase, value.appearance, value.bilirubin, value.casts, value.color))
    else:
        raise HealthCareException("Could not retrieve lab test listing.")


def do_list_pulse(args):
    url = _get_url(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=None)

    pulse_list = client.list_pulse()

    if pulse_list is not None:
        fmt = "%-15s %-15s %-15s %-15s"
        print(fmt % ('PATIENT HEX', 'PATIENT PKEY', 'PULSE', 'TIMESTAMP'))
        for key, value in pulse_list.items():
            print(fmt % (key, value.public_key, value.pulse, value.timestamp))
    else:
        raise HealthCareException("Could not retrieve pulse listing.")

# def do_list_claims(args):
#     url = _get_url(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=None)
#
#     claims_list = client.list_claims(auth_user=auth_user,
#                                      auth_password=auth_password)
#
#     if claims_list is not None:
#         fmt = "%-15s %-15s %-15s %-15s"
#         print(fmt % ('CLAIM HEX', 'CLAIM ID', 'CLINIC PKEY', 'PATIENT PKEY'))
#         for key, value in claims_list.items():
#             print(fmt % (key, value.claim_id, value.clinic_pkey, value.patient_pkey))
#     else:
#         raise HealthCareException("Could not retrieve claims listing.")
#
#
# def do_list_claim_details(args):
#     clinic_pkey = args.clinic_pkey
#     claim_id = args.claim_id
#     url = _get_url(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=None)
#
#     claim_details_list = client.list_claim_details(claim_id, clinic_pkey, auth_user=auth_user,
#                                                    auth_password=auth_password)
#
#     if claim_details_list is not None:
#         fmt = "%-15s %-15s %-15s %-15s %-15s %-15s"
#         print(fmt % ('EVENT HEX', 'CLAIM ID', 'CLINIC PKEY', 'EVENT', 'DESCRIPTION', 'EVENT TIME'))
#         for key, value in claim_details_list.items():
#             print(fmt % (key, value.claim_id, value.clinic_pkey, value.event, value.description, value.event_time))
#     else:
#         raise HealthCareException("Could not retrieve claim details listing.")


def do_create_clinic(args):
    name = args.name

    url = _get_url(args)
    keyfile = _generate_keyfile(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.create_clinic(
            name, wait=args.wait)
    else:
        response = client.create_clinic(name)

    print("Response: {}".format(response))


# def do_create_claim(args):
#     claim_id = args.claim_id
#     patient_pkey = args.patient_pkey
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.add_claim(
#             claim_id,
#             patient_pkey,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.add_claim(
#             claim_id,
#             patient_pkey,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))


def do_create_doctor(args):
    name = args.name
    surname = args.surname
    speciality = "Ortopeda"
    url = _get_url(args)
    keyfile = _generate_keyfile(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.create_doctor(
            name,
            surname,
            speciality,
            wait=args.wait)
    else:
        response = client.create_doctor(
            name,
            surname)

    print("Response: {}".format(response))


def do_create_patient(args):
    name = args.name
    surname = args.surname

    url = _get_url(args)
    keyfile = _generate_keyfile(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.create_patient(
            name,
            surname,
            wait=args.wait)
    else:
        response = client.create_patient(
            name,
            surname)

    print("Response: {}".format(response))


def do_add_lab_test(args):
    height = args.height
    weight = args.weight
    gender = args.gender
    a_g_ratio = args.a_g_ratio
    albumin = args.albumin
    alkaline_phosphatase = args.alkaline_phosphatase
    appearance = args.appearance
    bilirubin = args.bilirubin
    casts = args.casts
    color = args.color

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.add_lab_test(
            height,
            weight,
            gender,
            a_g_ratio,
            albumin,
            alkaline_phosphatase,
            appearance,
            bilirubin,
            casts,
            color,
            wait=args.wait)
    else:
        response = client.add_lab_test(
            height,
            weight,
            gender,
            a_g_ratio,
            albumin,
            alkaline_phosphatase,
            appearance,
            bilirubin,
            casts,
            color)

    print("Response: {}".format(response))


def do_add_pulse(args):
    pulse = args.pulse
    timestamp = args.timestamp

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    # auth_user, auth_password = _get_auth_info(args)

    client = HealthCareClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.add_pulse(
            pulse,
            timestamp,
            wait=args.wait)
    else:
        response = client.add_pulse(
            pulse,
            timestamp)

    print("Response: {}".format(response))
# def do_assign_doctor(args):
#     claim_id = args.claim_id
#     doctor_pkey = args.doctor_pkey
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.assign_doctor(
#             claim_id,
#             doctor_pkey,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.assign_doctor(
#             claim_id,
#             doctor_pkey,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))
#
#
# def do_first_visit(args):
#     claim_id = args.claim_id
#     description = args.description
#     doctor_pkey = args.doctor_pkey
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.first_visit(
#             claim_id=claim_id,
#             description=description,
#             doctor_pkey=doctor_pkey,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.first_visit(
#             claim_id=claim_id,
#             description=description,
#             doctor_pkey=doctor_pkey,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))
#
#
# def do_pass_tests(args):
#     claim_id = args.claim_id
#     description = args.description
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.pass_tests(
#             claim_id=claim_id,
#             description=description,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.pass_tests(
#             claim_id=claim_id,
#             description=description,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))
#
#
# def do_attend_procedures(args):
#     claim_id = args.claim_id
#     description = args.description
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.attend_procedures(
#             claim_id=claim_id,
#             description=description,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.attend_procedures(
#             claim_id=claim_id,
#             description=description,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))
#
#
# def do_eat_pills(args):
#     claim_id = args.claim_id
#     description = args.description
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.eat_pills(
#             claim_id=claim_id,
#             description=description,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.eat_pills(
#             claim_id=claim_id,
#             description=description,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))
#
#
# def do_next_visit(args):
#     claim_id = args.claim_id
#     description = args.description
#     doctor_pkey = args.doctor_pkey
#
#     url = _get_url(args)
#     keyfile = _get_keyfile(args)
#     auth_user, auth_password = _get_auth_info(args)
#
#     client = HealthCareClient(base_url=url, keyfile=keyfile)
#
#     if args.wait and args.wait > 0:
#         response = client.next_visit(
#             claim_id=claim_id,
#             description=description,
#             doctor_pkey=doctor_pkey,
#             wait=args.wait,
#             auth_user=auth_user,
#             auth_password=auth_password)
#     else:
#         response = client.next_visit(
#             claim_id=claim_id,
#             description=description,
#             doctor_pkey=doctor_pkey,
#             auth_user=auth_user,
#             auth_password=auth_password)
#
#     print("Response: {}".format(response))


def _get_url(args):
    return DEFAULT_URL if args.url is None else args.url


# def _get_auth_info(args):
#     auth_user = args.auth_user
#     auth_password = args.auth_password
#     if auth_user is not None and auth_password is None:
#         auth_password = getpass.getpass(prompt="Auth Password: ")
#
#     return auth_user, auth_password


def _get_keyfile(args):
    name = getpass.getuser() if args.name is None else args.name
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, name)


def _generate_keyfile(args):
    keyfilename = _get_keyfile(args)
    if not (os.path.exists(keyfilename) and os.path.isfile(keyfilename)):
        os.makedirs(os.path.dirname(keyfilename), exist_ok=True)
        keyfile = open(keyfilename, "w")
        keyfile.write(_make_key())
        keyfile.close()
    return keyfilename


def _make_key():
    context = create_context('secp256k1')
    private_key = context.new_random_private_key()
    # signer = CryptoFactory(context).new_signer(private_key)
    # return signer
    return private_key.as_hex()


def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)

    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose

    setup_loggers(verbose_level=verbose_level)

    if args.command == 'create_clinic':
        do_create_clinic(args)
    # elif args.command == 'create_claim':
    #     do_create_claim(args)
    elif args.command == 'create_doctor':
        do_create_doctor(args)
    elif args.command == 'create_patient':
        do_create_patient(args)
    elif args.command == 'add_lab_test':
        do_add_lab_test(args)
    elif args.command == 'add_pulse':
        do_add_pulse(args)
    # elif args.command == 'assign_doctor':
    #     do_assign_doctor(args)
    # elif args.command == 'pass_tests':
    #     do_pass_tests(args)
    # elif args.command == 'attend_procedures':
    #     do_attend_procedures(args)
    # elif args.command == 'eat_pills':
    #     do_eat_pills(args)
    # elif args.command == 'next_visit':
    #     do_next_visit(args)
    # elif args.command == 'first_visit':
    #     do_first_visit(args)
    elif args.command == 'list_clinics':
        do_list_clinics(args)
    elif args.command == 'list_doctors':
        do_list_doctors(args)
    elif args.command == 'list_patients':
        do_list_patients(args)
    elif args.command == 'list_lab_test':
        do_list_lab_test(args)
    elif args.command == 'list_pulse':
        do_list_pulse(args)

    # elif args.command == 'list_claims':
    #     do_list_claims(args)
    # elif args.command == 'list_claim_details':
    #     do_list_claim_details(args)
    else:
        raise HealthCareException("invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except HealthCareException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
