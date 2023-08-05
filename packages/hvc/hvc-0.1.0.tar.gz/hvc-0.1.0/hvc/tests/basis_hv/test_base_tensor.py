
import pytest
import torch

from hvc import VSATensor


class TestVSATensor:
    def test_empty(self):
        with pytest.raises(NotImplementedError):
            VSATensor.empty(4, 525)

    def test_identity(self):
        with pytest.raises(NotImplementedError):
            VSATensor.identity(4, 525)

    def test_random(self):
        with pytest.raises(NotImplementedError):
            VSATensor.random(4, 525)

    def test_bundle(self):
        a = torch.randn(100).as_subclass(VSATensor)
        b = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.bundle(b)

    def test_multibundle(self):
        a = torch.randn(10, 100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.multibundle()

    def test_bind(self):
        a = torch.randn(100).as_subclass(VSATensor)
        b = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.bind(b)

    def test_multibind(self):
        a = torch.randn(10, 100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.multibind()

    def test_inverse(self):
        a = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.inverse()

    def test_negative(self):
        a = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.negative()

    def test_permute(self):
        a = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.permute()

    def test_dot_similarity(self):
        a = torch.randn(100).as_subclass(VSATensor)
        b = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.dot_similarity(b)

    def test_cosine_similarity(self):
        a = torch.randn(100).as_subclass(VSATensor)
        b = torch.randn(100).as_subclass(VSATensor)

        with pytest.raises(NotImplementedError):
            a.cosine_similarity(b)
