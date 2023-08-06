"""
Copyright (c) 2022 Inqana Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from datetime import datetime, timedelta

from nqsdk.abstract.quotas import ProviderDynamicQuota, ProviderStaticQuota
from nqsdk.enums import QuotaIdentityType


class RetryAfterQuota(ProviderDynamicQuota):
    @classmethod
    def identity_type(cls) -> QuotaIdentityType:
        return QuotaIdentityType.AUTH_ENTITY

    def __init__(self, delay: int):
        self._until = datetime.now() + timedelta(seconds=delay)

    @property
    def until(self) -> datetime:
        return self._until


class PerSecondQuota(ProviderStaticQuota):
    @classmethod
    def identity_type(cls) -> QuotaIdentityType:
        return QuotaIdentityType.AUTH_ENTITY

    @property
    def limit(self) -> int:
        return 30

    @property
    def frame(self) -> int:
        return 1
