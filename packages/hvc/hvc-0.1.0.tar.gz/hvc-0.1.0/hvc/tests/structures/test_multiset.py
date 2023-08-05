
import pytest
import torch
import string

from hvc import structures, functional
from hvc import MAPTensor

seed = 2147483644
letters = list(string.ascii_lowercase)


class TestMultiset:
    def test_creation_dim(self):
        M = structures.Multiset(10000)
        assert torch.allclose(M.value, torch.zeros(10000))

    def test_creation_tensor(self):
        generator = torch.Generator()
        generator.manual_seed(seed)
        keys_hv = functional.random(len(letters), 10000, generator=generator)
        multiset = functional.multiset(keys_hv)

        M = structures.Multiset(multiset)
        assert torch.allclose(M.value, multiset)

    def test_generator(self):
        generator = torch.Generator()
        generator.manual_seed(seed)
        hv1 = functional.random(60, 10000, generator=generator)

        generator = torch.Generator()
        generator.manual_seed(seed)
        hv2 = functional.random(60, 10000, generator=generator)

        assert (hv1 == hv2).min().item()

    def test_add(self):
        keys_hv = MAPTensor(
            [
                [1.0, -1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, -1.0, 1.0],
                [1.0, 1.0, 1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, 1.0, -1.0],
                [1.0, -1.0, -1.0, 1.0, -1.0],
                [1.0, 1.0, 1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, -1.0],
                [-1.0, -1.0, -1.0, -1.0, -1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, -1.0, -1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, -1.0],
                [1.0, 1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0, -1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, -1.0, 1.0],
                [1.0, 1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, 1.0, -1.0, -1.0, 1.0],
            ]
        )
        M = structures.Multiset(5)

        M.add(keys_hv[0])
        assert torch.allclose(M.value, MAPTensor([1.0, -1.0, 1.0, 1.0, 1.0]))

        M.add(keys_hv[1])
        assert torch.allclose(M.value, MAPTensor([0.0, -2.0, 2.0, 2.0, 2.0]))

        M.add(keys_hv[2])
        assert torch.allclose(M.value, MAPTensor([1.0, -1.0, 3.0, 1.0, 3.0]))

    def test_remove(self):
        generator = torch.Generator()
        generator.manual_seed(seed)
        keys_hv = functional.random(len(letters), 1000, generator=generator)
        M = structures.Multiset(1000)

        M.add(keys_hv[0])
        M.add(keys_hv[1])

        assert M.contains(keys_hv[0]) > torch.tensor([0.5])

        M.remove(keys_hv[0])
        assert M.contains(keys_hv[0]) < torch.tensor([0.1])
        assert M.contains(keys_hv[1]) > torch.tensor([0.5])
        assert M.remove(keys_hv[0]) is None

    def test_contains(self):
        generator = torch.Generator()
        generator.manual_seed(seed)
        keys_hv = functional.random(len(letters), 1000, generator=generator)
        M = structures.Multiset(1000)

        M.add(keys_hv[0])
        M.add(keys_hv[0])
        M.add(keys_hv[0])
        M.add(keys_hv[1])
        assert M.contains(keys_hv[0]) > torch.tensor([0.8])
        M.remove(keys_hv[0])
        assert M.contains(keys_hv[0]) > torch.tensor([0.8])
        M.remove(keys_hv[0])
        assert M.contains(keys_hv[0]) > torch.tensor([0.7])
        M.remove(keys_hv[0])
        assert M.contains(keys_hv[0]) < torch.tensor([0.1])
        M.remove(keys_hv[1])
        assert M.contains(keys_hv[1]) < torch.tensor([0.1])

    def test_length(self):
        generator = torch.Generator()
        generator.manual_seed(seed)
        keys_hv = functional.random(len(letters), 4, generator=generator)
        M = structures.Multiset(4)

        M.add(keys_hv[0])
        M.add(keys_hv[0])
        M.add(keys_hv[1])

        assert len(M) == 3
        M.remove(keys_hv[0])

        assert len(M) == 2

    def test_clear(self):
        generator = torch.Generator()
        generator.manual_seed(seed)
        keys_hv = functional.random(len(letters), 4, generator=generator)
        M = structures.Multiset(4)

        M.add(keys_hv[0])
        M.add(keys_hv[0])
        M.add(keys_hv[1])

        M.clear()

        assert M.contains(keys_hv[0]) < torch.tensor([0.1])
        assert M.contains(keys_hv[1]) < torch.tensor([0.1])

        M.add(keys_hv[0])
        assert M.contains(keys_hv[0]) > torch.tensor([0.8])

    def test_from_ngrams(self):
        keys_hv = MAPTensor(
            [
                [1.0, -1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, -1.0, 1.0],
                [1.0, 1.0, 1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, 1.0, -1.0],
                [1.0, -1.0, -1.0, 1.0, -1.0],
                [1.0, 1.0, 1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, -1.0],
                [-1.0, -1.0, -1.0, -1.0, -1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, -1.0, -1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, -1.0],
                [1.0, 1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0, -1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, -1.0, 1.0],
                [1.0, 1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, 1.0, -1.0, -1.0, 1.0],
            ]
        )

        M = structures.Multiset.from_ngrams(keys_hv)
        assert torch.allclose(M.value, MAPTensor([6.0, 0.0, -10.0, 8.0, -4.0]))

    def test_from_tensor(self):
        keys_hv = MAPTensor(
            [
                [1.0, -1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, -1.0, 1.0],
                [1.0, 1.0, 1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, -1.0, -1.0, 1.0, -1.0],
                [1.0, -1.0, -1.0, 1.0, -1.0],
                [1.0, 1.0, 1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, -1.0],
                [-1.0, -1.0, -1.0, -1.0, -1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, -1.0, -1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, -1.0],
                [1.0, 1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, 1.0, -1.0],
                [-1.0, -1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, -1.0],
                [-1.0, 1.0, -1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [-1.0, -1.0, 1.0, -1.0, 1.0],
                [1.0, 1.0, -1.0, 1.0, 1.0],
                [-1.0, -1.0, -1.0, -1.0, 1.0],
                [-1.0, 1.0, -1.0, -1.0, 1.0],
            ]
        )

        M = structures.Multiset.from_tensor(keys_hv)
        assert torch.allclose(M.value, MAPTensor([-6.0, 0.0, -4.0, 2.0, 6.0]))
