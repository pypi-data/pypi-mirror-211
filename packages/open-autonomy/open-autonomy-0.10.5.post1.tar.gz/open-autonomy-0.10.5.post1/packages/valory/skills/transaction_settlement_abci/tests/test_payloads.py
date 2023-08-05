# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Test the payloads of the skill."""

# pylint: skip-file

from typing import Optional

import pytest

from packages.valory.skills.transaction_settlement_abci.payloads import (
    CheckTransactionHistoryPayload,
    FinalizationTxPayload,
    RandomnessPayload,
    ResetPayload,
    SelectKeeperPayload,
    SignaturePayload,
    SynchronizeLateMessagesPayload,
    ValidatePayload,
)


def test_randomness_payload() -> None:
    """Test `RandomnessPayload`."""

    payload = RandomnessPayload(sender="sender", round_id=1, randomness="test")

    assert payload.round_id == 1
    assert payload.randomness == "test"
    assert payload.data == {"round_id": 1, "randomness": "test"}


def test_select_keeper_payload() -> None:
    """Test `SelectKeeperPayload`."""

    payload = SelectKeeperPayload(sender="sender", keepers="test")

    assert payload.keepers == "test"
    assert payload.data == {"keepers": "test"}


@pytest.mark.parametrize("vote", (None, True, False))
def test_validate_payload(vote: Optional[bool]) -> None:
    """Test `ValidatePayload`."""

    payload = ValidatePayload(sender="sender", vote=vote)

    assert payload.vote is vote
    assert payload.data == {"vote": vote}


def test_tx_history_payload() -> None:
    """Test `CheckTransactionHistoryPayload`."""

    payload = CheckTransactionHistoryPayload(sender="sender", verified_res="test")

    assert payload.verified_res == "test"
    assert payload.data == {"verified_res": "test"}


def test_synchronize_payload() -> None:
    """Test `SynchronizeLateMessagesPayload`."""

    tx_hashes = "test"
    payload = SynchronizeLateMessagesPayload(sender="sender", tx_hashes=tx_hashes)

    assert payload.tx_hashes == tx_hashes
    assert payload.data == {"tx_hashes": tx_hashes}


def test_signature_payload() -> None:
    """Test `SignaturePayload`."""

    payload = SignaturePayload(sender="sender", signature="sign")

    assert payload.signature == "sign"
    assert payload.data == {"signature": "sign"}


def test_finalization_tx_payload() -> None:
    """Test `FinalizationTxPayload`."""

    payload = FinalizationTxPayload(
        sender="sender",
        tx_data={
            "tx_digest": "hash",
            "nonce": 0,
            "max_fee_per_gas": 0,
            "max_priority_fee_per_gas": 0,
        },
    )

    assert payload.data == {
        "tx_data": {
            "tx_digest": "hash",
            "nonce": 0,
            "max_fee_per_gas": 0,
            "max_priority_fee_per_gas": 0,
        }
    }


def test_reset_payload() -> None:
    """Test `ResetPayload`."""

    payload = ResetPayload(sender="sender", period_count=1)

    assert payload.period_count == 1
    assert payload.data == {"period_count": 1}
