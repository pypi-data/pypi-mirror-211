import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.node.requests.validate_bonds import ValidateBondsRequest, NodeValidateBondsParams


class ValidateBondsRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x01\x08\xff\xff\x0a\x00\x00\x00\x00\x0b\x01\x00\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedNode_ValidateBonds',
            'data': {
                'msgId': 'validateBondsTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'nodes': [
                            {
                                'bondAddr': 10,
                                'mid': 0
                            },
                            {
                                'bondAddr': 11,
                                'mid': 1
                            }
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'single_pair',
            [NodeValidateBondsParams(bondAddr=1, mid=2164554855)],
            b'\x01\x00\x01\x08\xff\xff\x01\x67\x7c\x04\x81'
        ],
        [
            'three_pairs',
            [
                NodeValidateBondsParams(bondAddr=1, mid=0),
                NodeValidateBondsParams(bondAddr=2, mid=2164554855),
                NodeValidateBondsParams(bondAddr=3, mid=2164554771),
            ],
            b'\x01\x00\x01\x08\xff\xff\x01\x00\x00\x00\x00\x02\x67\x7c\x04\x81\x03\x13\x7c\x04\x81'
        ]
    ])
    def test_to_dpa(self, _, params, expected):
        request = ValidateBondsRequest(nadr=1, nodes=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_pair',
            [NodeValidateBondsParams(bondAddr=1, mid=2164554855)],
        ],
        [
            'three_pairs',
            [
                NodeValidateBondsParams(bondAddr=1, mid=0),
                NodeValidateBondsParams(bondAddr=2, mid=2164554855),
                NodeValidateBondsParams(bondAddr=3, mid=2164554771),
            ],
        ]
    ])
    def test_to_json(self, _, params):
        request = ValidateBondsRequest(nadr=1, nodes=params, msgid='validateBondsTest')
        self.json['data']['req']['param']['nodes'] = [{'bondAddr': node.bondAddr, 'mid': node.mid} for node in params]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            'single_pair',
            [NodeValidateBondsParams(bondAddr=1, mid=2164554855)],
            b'\x01\x00\x01\x08\xff\xff\x01\x67\x7c\x04\x81'
        ],
        [
            'three_pairs',
            [
                NodeValidateBondsParams(bondAddr=1, mid=0),
                NodeValidateBondsParams(bondAddr=2, mid=2164554855),
                NodeValidateBondsParams(bondAddr=3, mid=2164554771),
            ],
            b'\x01\x00\x01\x08\xff\xff\x01\x00\x00\x00\x00\x02\x67\x7c\x04\x81\x03\x13\x7c\x04\x81'
        ]
    ])
    def test_set_nodes(self, _, params, dpa):
        nodes = [NodeValidateBondsParams(bondAddr=10, mid=0), NodeValidateBondsParams(bondAddr=11, mid=1)]
        request = ValidateBondsRequest(nadr=1, nodes=nodes, msgid='validateBondsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.set_nodes(params)
        self.json['data']['req']['param']['nodes'] = [{'bondAddr': node.bondAddr, 'mid': node.mid} for node in params]
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [1, -1],
        [256, 10],
        [2, 4294967297],
    ])
    def test_invalid_param_members(self, bond_addr, mid):
        with self.assertRaises(RequestParameterInvalidValueError):
            NodeValidateBondsParams(bondAddr=bond_addr, mid=mid)

    @parameterized.expand([
        [[NodeValidateBondsParams(bondAddr=random.randint(0, 255), mid=random.randint(0, 0xFFFFFFFF))] * 12]
    ])
    def test_invalid_pair_count(self, params: List[NodeValidateBondsParams]):
        with self.assertRaises(RequestParameterInvalidValueError):
            ValidateBondsRequest(nadr=1, nodes=params)
