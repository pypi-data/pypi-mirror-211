import numpy as np
import pytest
import tskit
import msprime

import tsinfer
import sc2ts
from sc2ts.inference import Matcher as SequentialExtender


def assert_variants_equal(vars1, vars2, allele_shuffle=False):
    assert vars1.num_sites == vars2.num_sites
    assert vars1.num_samples == vars2.num_samples
    for var1, var2 in zip(vars1.variants(), vars2.variants()):
        if allele_shuffle:
            h1 = np.array(var1.alleles)[var1.genotypes]
            h2 = np.array(var2.alleles)[var2.genotypes]
            assert np.all(h1 == h2)
        else:
            assert var1.alleles == var2.alleles
            assert np.all(var1.genotypes == var2.genotypes)


@pytest.mark.skip()
class TestExtend:
    @pytest.mark.parametrize("num_samples", range(1, 5))
    @pytest.mark.parametrize("num_sites", range(1, 5))
    def test_single_binary_haplotype_one_generation(self, num_samples, num_sites):
        with tsinfer.SampleData(sequence_length=num_sites) as sd:
            for j in range(num_sites):
                sd.add_site(j, [1] * num_samples)
        extender = SequentialExtender(sd)
        ts = extender.extend(np.arange(num_samples))
        assert_variants_equal(ts, sd)

    @pytest.mark.parametrize("num_samples", range(1, 5))
    @pytest.mark.parametrize("num_sites", range(1, 5))
    def test_single_binary_haplotype_two_epochs(self, num_samples, num_sites):
        with tsinfer.SampleData(sequence_length=num_sites) as sd:
            for j in range(num_sites):
                sd.add_site(j, [1] * num_samples)
        extender = SequentialExtender(sd)
        ts = extender.extend(np.arange(num_samples))

        extender = SequentialExtender(sd, ancestors_ts=ts)
        ts = extender.extend(np.arange(num_samples))
        assert ts.num_samples == 2 * num_samples
        assert np.all(ts.genotype_matrix() == 1)

    @pytest.mark.parametrize("k", range(1, 5))
    def test_single_binary_haplotype_k_generations(self, k):
        num_sites = 5
        num_samples = 4
        with tsinfer.SampleData(sequence_length=num_sites) as sd:
            for j in range(num_sites):
                sd.add_site(j, [1] * (num_samples * k))

        extender = SequentialExtender(sd)
        for _ in range(k):
            ts = extender.extend(np.arange(num_samples) * k)
        assert_variants_equal(ts, sd)

    @pytest.mark.parametrize("k", range(1, 5))
    def test_single_binary_haplotype_k_generations_two_epochs(self, k):
        num_sites = 5
        num_samples = 4
        with tsinfer.SampleData(sequence_length=num_sites) as sd:
            for j in range(num_sites):
                sd.add_site(j, [1] * (num_samples * k))

        extender = SequentialExtender(sd)
        for _ in range(k):
            ts = extender.extend(np.arange(num_samples) * k)
            # last num_samples should all have time 0
            assert np.all(ts.tables.nodes.time[ts.samples()[-num_samples:]] == 0)
        extender = SequentialExtender(sd, ts)
        for _ in range(k):
            ts = extender.extend(np.arange(num_samples) * k)
            assert np.all(ts.tables.nodes.time[ts.samples()[-num_samples:]] == 0)
        assert ts.num_samples == 2 * num_samples * k
        assert np.all(ts.genotype_matrix() == 1)

    def test_single_haplotype_4_alleles(self):
        num_sites = 3
        with tsinfer.SampleData(sequence_length=num_sites) as sd:
            for j in range(num_sites):
                sd.add_site(j, [0, 1, 2, 3], alleles="ACGT")

        extender = SequentialExtender(sd)
        ts = extender.extend(np.arange(4))
        assert_variants_equal(ts, sd)

    @pytest.mark.parametrize("k", range(4, 9))
    def test_single_site_4_alleles_rotating(self, k):
        genotypes = np.zeros(k, dtype=int)
        for j in range(k):
            genotypes[j] = j % 4
        with tsinfer.SampleData(sequence_length=1) as sd:
            sd.add_site(0, genotypes, alleles="ACGT")

        extender = SequentialExtender(sd)
        for j in range(k):
            ts = extender.extend([j])
        assert ts.num_mutations == 3
        assert_variants_equal(ts, sd)

    @pytest.mark.parametrize("num_generations", range(1, 5))
    @pytest.mark.parametrize("samples_per_generation", [1, 2, 13])
    @pytest.mark.parametrize("num_sites", [1, 4, 10, 100])
    def test_random_data(self, num_generations, samples_per_generation, num_sites):
        rng = np.random.default_rng(42)
        num_samples = num_generations * samples_per_generation
        with tsinfer.SampleData(sequence_length=num_sites) as sd:
            for j in range(num_samples):
                sd.add_individual(ploidy=1, metadata={"ind_id": j})
            for j in range(num_sites):
                genotypes = rng.integers(0, 4, size=num_samples)
                sd.add_site(j, genotypes, alleles="ACGT")

        extender = SequentialExtender(sd)
        offset = 0
        for _ in range(num_generations):
            next_offset = offset + samples_per_generation
            ts = extender.extend(np.arange(offset, next_offset))
            assert ts.num_samples == next_offset
            offset = next_offset

        assert ts.num_sites == sd.num_sites
        assert ts.num_samples == sd.num_samples
        for var1, var2 in zip(ts.variants(alleles=("A", "C", "G", "T")), sd.variants()):
            assert var1.alleles == var2.alleles
            assert np.all(var1.genotypes == var2.genotypes)
        for j, u in enumerate(ts.samples()):
            assert ts.node(u).metadata == {"ind_id": j}

    @pytest.mark.parametrize("num_generations", [1, 2, 5])
    @pytest.mark.parametrize("samples_per_generation", [1, 2, 13])
    @pytest.mark.parametrize("num_epochs", range(1, 4))
    def test_random_data_multi_epoch_fixed_sites(
        self, num_generations, samples_per_generation, num_epochs
    ):
        rng = np.random.default_rng(142)
        num_sites = 10
        ancestors_ts = None
        total_samples = num_epochs * num_generations * samples_per_generation
        G = rng.integers(0, 4, size=(total_samples, num_sites))
        for epoch in range(num_epochs):
            num_samples = num_generations * samples_per_generation
            epoch_start = epoch * num_samples
            genotypes = G[epoch_start : epoch_start + num_samples]
            with tsinfer.SampleData(sequence_length=num_sites) as sd:
                # Store the genotypes with the individual metadata so
                # we can compare later.
                for j in range(num_samples):
                    sd.add_individual(
                        ploidy=1,
                        metadata={
                            "epoch": epoch,
                            "ind_id": (epoch, j),
                            "genotypes": list(map(int, genotypes[j])),
                        },
                    )
                for j in range(num_sites):
                    sd.add_site(j, genotypes[:, j], alleles="ACGT")
            extender = SequentialExtender(sd, ancestors_ts)
            offset = 0
            for _ in range(num_generations):
                next_offset = offset + samples_per_generation
                ts = extender.extend(np.arange(offset, next_offset))
                offset = next_offset
            assert ts.num_sites == num_sites
            assert ts.num_samples == num_samples * (1 + epoch)
            ancestors_ts = ts
        # Do we round-trip all the data?
        for j, u in enumerate(ts.samples()):
            node = ts.node(u)
            md = node.metadata
            assert md["ind_id"] == [j // num_samples, j % num_samples]
            assert np.array_equal(md["genotypes"], G[j])

    def test_single_sample_metadata(self):
        with tsinfer.SampleData(sequence_length=1) as sd:
            sd.add_individual(ploidy=1, metadata={"x": 1})
            sd.add_site(0, [1])
        extender = SequentialExtender(sd)
        ts = extender.extend([0])
        assert_variants_equal(ts, sd)
        assert ts.node(ts.samples()[0]).metadata == {"x": 1}

    @pytest.mark.parametrize("num_generations", range(1, 5))
    def test_stick(self, num_generations):
        # We have a stick tree where the single mutation for a given site
        # happens on one branch and they accumulate over time.
        H = np.zeros((num_generations, num_generations), dtype=int)
        a = np.zeros(num_generations, dtype=int)
        for j in range(num_generations):
            a[j] = 1
            H[j] = a
        with tsinfer.SampleData(sequence_length=num_generations) as sd:
            for j in range(num_generations):
                sd.add_site(j, H[:, j])
        extender = SequentialExtender(sd)
        for j in range(num_generations):
            ts = extender.extend([j])
            assert ts.num_samples == j + 1
        assert ts.num_mutations == num_generations
        assert ts.num_edges == num_generations + 1

    @pytest.mark.parametrize("num_generations", range(1, 5))
    def test_all_zeros(self, num_generations):
        # all the haplotypes are 0s and should just copy directly from
        # the same root.
        a = np.zeros(2 * num_generations, dtype=int)
        with tsinfer.SampleData(sequence_length=num_generations) as sd:
            sd.add_site(0, a)
        extender = SequentialExtender(sd)
        for j in range(num_generations):
            ts = extender.extend([2 * j, 2 * j + 1])
            # assert ts.num_samples == 2 * j + 1
        assert ts.num_mutations == 0
        assert ts.num_trees == 1
        tree = ts.first()
        parents = {tree.parent(u) for u in ts.samples()}
        assert len(parents) == 1

    def test_all_zeros_time_increment(self):
        a = np.zeros(2 * 2, dtype=int)
        with tsinfer.SampleData(sequence_length=2) as sd:
            sd.add_site(0, a)
        extender = SequentialExtender(sd)
        ts = extender.extend([0, 1], time_increment=5)
        np.testing.assert_array_equal(ts.nodes_time, [6, 5, 0, 0])
        ts = extender.extend([2, 3], time_increment=2)
        np.testing.assert_array_equal(ts.nodes_time, [8, 7, 2, 2, 0, 0])

        extender = SequentialExtender(sd, ancestors_ts=ts)
        ts = extender.extend([0, 1], time_increment=3)
        np.testing.assert_array_equal(ts.nodes_time, [11, 10, 5, 5, 3, 3, 0, 0])
        assert ts.time_units == tskit.TIME_UNITS_UNCALIBRATED

        ts = extender.extend([0, 1], time_increment=0.1)
        np.testing.assert_array_equal(
            ts.nodes_time, [11.1, 10.1, 5.1, 5.1, 3.1, 3.1, 0.1, 0.1, 0, 0]
        )
        assert ts.time_units == tskit.TIME_UNITS_UNCALIBRATED

    def test_all_zeros_time_units(self):
        a = np.zeros(2 * 2, dtype=int)
        with tsinfer.SampleData(sequence_length=2) as sd:
            sd.add_site(0, a)
        time_units = "days_ago"
        extender = SequentialExtender(sd, time_units=time_units)
        ts = extender.extend([0, 1])
        assert ts.time_units == time_units
        ts = extender.extend([2, 3])
        assert ts.time_units == time_units

        # Specifying different time_units gives an error
        with pytest.raises(ValueError, match="time_units"):
            extender = SequentialExtender(sd, ancestors_ts=ts)
        with pytest.raises(ValueError, match="time_units"):
            extender = SequentialExtender(sd, ancestors_ts=ts, time_units="stuff")

        extender = SequentialExtender(sd, ancestors_ts=ts, time_units=time_units)
        ts = extender.extend([0, 1])
        assert ts.time_units == time_units
        ts = extender.extend([2, 3])
        assert ts.time_units == time_units


@pytest.mark.skip()
class TestExtendPathCompression:
    def example(self):
        with tsinfer.SampleData(sequence_length=4) as sd:
            sd.add_site(0, [0, 1, 1, 1])
            sd.add_site(1, [0, 1, 1, 1])
            sd.add_site(2, [1, 0, 1, 1])
            sd.add_site(3, [1, 0, 2, 1], alleles=("0", "1", "2"))
            return sd

    def test_simple_path_compression_case(self):
        sd = self.example()
        extender = SequentialExtender(sd)
        ts = extender.extend([0, 1])
        # NOTE we'd really like to get rid of this vestigial node 0 but
        # the low-level code won't work without it, so until it's
        # gone it's simplest to just live with it and update the test
        # cases later.

        # 2.00┊  0  ┊
        #     ┊  ┃  ┊
        # 1.00┊  1  ┊
        #     ┊ ┏┻┓ ┊
        # 0.00┊ 2 3 ┊
        #     0     4
        assert ts.num_trees == 1
        assert ts.num_nodes == 4
        assert ts.first().parent_dict == {2: 1, 3: 1, 1: 0}

        ts = extender.extend([2, 3])
        # 3.00┊   0   ┊   0   ┊
        #     ┊   ┃   ┊   ┃   ┊
        # 2.00┊   1   ┊   1   ┊
        #     ┊ ┏━┻┓  ┊ ┏━┻┓  ┊
        # 1.00┊ 2  3  ┊ 3  2  ┊
        #     ┊    ┃  ┊    ┃  ┊
        # 1.00┊    6  ┊    6  ┊
        #     ┊   ┏┻┓ ┊   ┏┻┓ ┊
        # 0.00┊   4 5 ┊   4 5 ┊
        #     0       2       4

        assert ts.num_trees == 2
        assert ts.num_nodes == 7
        assert ts.node(6).flags == tsinfer.NODE_IS_PC_ANCESTOR
        assert ts.first().parent_dict == {2: 1, 3: 1, 1: 0, 6: 3, 4: 6, 5: 6}
        assert ts.last().parent_dict == {2: 1, 3: 1, 1: 0, 6: 2, 4: 6, 5: 6}
        assert_variants_equal(ts, sd)

    def test_simple_path_compression_case_no_pc(self):
        sd = self.example()

        extender = SequentialExtender(sd)
        ts = extender.extend([0, 1])
        assert ts.num_trees == 1
        assert ts.num_nodes == 4
        assert ts.first().parent_dict == {2: 1, 3: 1, 1: 0}

        ts = extender.extend([2, 3], path_compression=False)
        # 3.00┊   0   ┊   0   ┊
        #     ┊   ┃   ┊   ┃   ┊
        # 2.00┊   1   ┊   1   ┊
        #     ┊ ┏━┻┓  ┊ ┏━┻┓  ┊
        # 1.00┊ 2  3  ┊ 3  2  ┊
        #     ┊   ┏┻┓ ┊   ┏┻┓ ┊
        # 0.00┊   4 5 ┊   4 5 ┊
        #     0       2       4
        assert ts.num_trees == 2
        assert ts.num_nodes == 6
        assert ts.first().parent_dict == {2: 1, 3: 1, 1: 0, 4: 3, 5: 3}
        assert ts.last().parent_dict == {2: 1, 3: 1, 1: 0, 4: 2, 5: 2}
        assert_variants_equal(ts, sd)


@pytest.mark.skip()
class TestExtendIdenticalSequences:
    def test_single_site_one_generation(self):
        with tsinfer.SampleData(sequence_length=1) as sd:
            sd.add_site(0, [1, 1])
        extender = SequentialExtender(sd)
        ts = extender.extend([0, 1])

        # 2.00┊  0  ┊
        #     ┊  ┃  ┊
        # 1.00┊  1  ┊
        #     ┊  ┃  ┊
        # 0.01┊  4  ┊
        #     ┊ ┏┻┓ ┊
        # 0.00┊ 2 3 ┊
        #     0     1
        assert ts.num_trees == 1
        assert ts.num_nodes == 5
        assert ts.first().parent_dict == {2: 4, 3: 4, 4: 1, 1: 0}
        assert ts.node(4).flags == tsinfer.NODE_IS_IDENTICAL_SAMPLE_ANCESTOR

        assert_variants_equal(ts, sd)

    def test_two_haplotypes_one_generation(self):
        alleles = ("A", "C", "G")
        with tsinfer.SampleData(sequence_length=2) as sd:
            sd.add_site(0, [1, 1, 2, 2], alleles=alleles)
            sd.add_site(1, [1, 1, 2, 2], alleles=alleles)
        extender = SequentialExtender(sd)
        ts = extender.extend([0, 1, 2, 3])

        # 2.00┊    0    ┊
        #     ┊    ┃    ┊
        # 1.00┊    1    ┊
        #     ┊  ┏━┻━┓  ┊
        # 0.00┊  6   7  ┊
        #     ┊ ┏┻┓ ┏┻┓ ┊
        # 0.00┊ 2 3 4 5 ┊
        #     0         2
        assert ts.num_trees == 1
        assert ts.num_nodes == 8

        assert ts.first().parent_dict == {2: 6, 3: 6, 4: 7, 5: 7, 6: 1, 7: 1, 1: 0}
        assert ts.node(6).flags == tsinfer.NODE_IS_IDENTICAL_SAMPLE_ANCESTOR
        assert ts.node(7).flags == tsinfer.NODE_IS_IDENTICAL_SAMPLE_ANCESTOR

        assert_variants_equal(ts, sd)

    def test_two_haplotypes_two_generations(self):
        alleles = ("A", "C", "G")
        with tsinfer.SampleData(sequence_length=2) as sd:
            sd.add_site(0, [1, 1, 2, 2, 2, 2], alleles=alleles)
            sd.add_site(1, [1, 1, 2, 2, 2, 2], alleles=alleles)
        extender = SequentialExtender(sd)
        ts = extender.extend([0, 1, 2, 3])
        ts = extender.extend([4, 5])
        # We correctly see that there was a pre-existing exact match for
        # this haplotype and match against it.
        assert_variants_equal(ts, sd)
        # 3.00┊     0       ┊
        #     ┊     ┃       ┊
        # 2.00┊     1       ┊
        #     ┊  ┏━━┻━━┓    ┊
        # 1.00┊  6     7    ┊
        #     ┊ ┏┻┓ ┏━┳┻┳━┓ ┊
        # 1.00┊ 2 3 4 5 ┃ ┃ ┊
        #     ┊         ┃ ┃ ┊
        # 0.00┊         8 9 ┊
        #     0             2
        assert ts.first().parent_dict == {
            2: 6,
            3: 6,
            4: 7,
            5: 7,
            6: 1,
            7: 1,
            1: 0,
            8: 7,
            9: 7,
        }
        assert ts.node(6).flags == tsinfer.NODE_IS_IDENTICAL_SAMPLE_ANCESTOR
        assert ts.node(7).flags == tsinfer.NODE_IS_IDENTICAL_SAMPLE_ANCESTOR


@pytest.mark.skip()
class TestExtendLsParameters:
    def run(self, num_mismatches=None):

        with tsinfer.SampleData(sequence_length=6) as sd:
            sd.add_site(0, [0, 1, 1])
            sd.add_site(1, [1, 0, 1])
            sd.add_site(2, [0, 1, 1])
            sd.add_site(3, [1, 0, 1])
            sd.add_site(4, [0, 1, 1])
            sd.add_site(5, [1, 0, 1])

        extender = SequentialExtender(sd)
        for j in range(3):
            ts = extender.extend(
                [j],
                num_mismatches=num_mismatches,
                num_threads=0,
                engine=tsinfer.C_ENGINE,
            )
        return ts

    @pytest.mark.parametrize("mismatches", [None, 0, 0.5])
    def test_all_recombination(self, mismatches):
        ts = self.run(mismatches)
        # We have a recombination at every site and exactly one mutation per site.
        assert ts.num_trees == ts.num_sites
        assert ts.num_mutations == ts.num_sites

    @pytest.mark.parametrize("mismatches", [3, 3.1, 4, 100, 1000])
    def test_no_recombination(self, mismatches):
        ts = self.run(mismatches)
        assert ts.num_trees == 1
        assert ts.num_mutations == 9

    def test_one_mismatch(self):
        ts = self.run(1)
        # This is all quite tricky - not quite sure what to expect. Keep
        # lint happy for now
        assert ts is not None
        # print(ts.tables)
        # print()
        # print(ts.draw_text())
        # print(ts.tables.mutations[ts.tables.mutations.node == 4])
        # print(ts.tables.mutations)


def assert_sequences_equal(ts1, ts2):
    """
    Check that the variation data for the specifed tree sequences
    is identical.
    """
    ts1.tables.sites.assert_equals(ts2.tables.sites)
    for var1, var2 in zip(ts1.variants(), ts2.variants()):
        states1 = np.array(var1.alleles)[var1.genotypes]
        states2 = np.array(var2.alleles)[var2.genotypes]
        np.testing.assert_array_equal(states1, states2)


def prepare(tables):
    """
    Make changes needed for generic table collection to be used.
    """
    tables.mutations.metadata_schema = tskit.MetadataSchema.permissive_json()
    tables.nodes.metadata_schema = tskit.MetadataSchema.permissive_json()
    tables.sort()
    tables.build_index()
    tables.compute_mutation_parents()
    return tables.tree_sequence()


class TestCoalesceMutations:
    def test_no_mutations(self):
        # 1.00┊    4    ┊
        #     ┊ ┏━┳┻┳━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts1 = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        ts2 = sc2ts.inference.coalesce_mutations(ts1)
        ts1.tables.assert_equals(ts2.tables)

    def test_two_mutation_groups_one_parent(self):
        # 1.00┊    4    ┊
        #     ┊ ┏━┳┻┳━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=1, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=2, time=0, derived_state="G")
        tables.mutations.add_row(site=0, node=3, time=0, derived_state="G")
        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 2
        assert ts2.num_nodes == 7

    def test_two_mutation_groups_two_parents(self):
        # 2.00┊    6    ┊
        #     ┊  ┏━┻━┓  ┊
        # 1.00┊  4   5  ┊
        #     ┊ ┏┻┓ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_balanced(4, arity=2).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=0, derived_state="T")
        tables.mutations.add_row(site=0, node=1, derived_state="T")
        tables.mutations.add_row(site=0, node=2, derived_state="G")
        tables.mutations.add_row(site=0, node=3, derived_state="G")
        tables.compute_mutation_times()
        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 2
        assert ts2.num_nodes == 9

    def test_internal_sib(self):
        # 2.00┊   4   ┊
        #     ┊ ┏━┻┓  ┊
        # 1.00┊ ┃  3  ┊
        #     ┊ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 ┊
        #     0       1
        ts = tskit.Tree.generate_balanced(3, arity=2).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=0, derived_state="T")
        tables.mutations.add_row(site=0, node=3, derived_state="T")
        tables.compute_mutation_times()
        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 1
        assert ts2.num_nodes == 6

    def test_nested_mutation(self):
        # 1.00┊    4    ┊
        #     ┊ ┏━┳┻┳━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.sites.add_row(0.5, "A")
        tables.mutations.add_row(site=0, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=1, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=2, time=0, derived_state="T")
        tables.mutations.add_row(site=1, node=2, time=0, derived_state="G")
        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 2
        assert ts2.num_nodes == 6

    def test_conflicting_nested_mutations(self):
        # 1.00┊    4    ┊
        #     ┊ ┏━┳┻┳━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.sites.add_row(0.5, "A")
        tables.mutations.add_row(site=0, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=1, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=2, time=0, derived_state="G")
        tables.mutations.add_row(site=1, node=1, time=0, derived_state="T")
        tables.mutations.add_row(site=1, node=2, time=0, derived_state="G")
        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 4
        assert ts2.num_nodes == 6

    def test_node_in_multiple_mutation_sets(self):
        # 1.00┊    4    ┊
        #     ┊ ┏━┳┻┳━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        # Node 0 particpates in 3 different maximum sets.
        ts = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.sites.add_row(0.25, "A")
        tables.sites.add_row(0.75, "A")
        tables.mutations.add_row(site=0, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=1, time=0, derived_state="T")
        tables.mutations.add_row(site=1, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=1, node=2, time=0, derived_state="T")
        tables.mutations.add_row(site=2, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=2, node=2, time=0, derived_state="T")
        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 4
        assert ts2.num_nodes == 6

    def test_mutations_on_same_branch(self):
        # 1.00┊    4    ┊
        #     ┊ ┏━┳┻┳━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=0, node=0, time=0, derived_state="C", parent=0)
        ts = prepare(tables)

        with pytest.raises(ValueError, match="Multiple mutations"):
            sc2ts.inference.coalesce_mutations(ts)

    def test_mutation_parent(self):
        # 2.00┊   4   ┊
        #     ┊ ┏━┻┓  ┊
        # 1.00┊ ┃  3  ┊
        #     ┊ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 ┊
        #     0       1
        ts = tskit.Tree.generate_balanced(3, arity=2).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.sites.add_row(0.1, "A")
        tables.mutations.add_row(site=0, node=3, time=1, derived_state="T")
        tables.mutations.add_row(site=0, node=1, time=0, derived_state="G", parent=0)
        tables.mutations.add_row(site=0, node=2, time=0, derived_state="G", parent=0)
        # Site 1 has a complicated mutation pattern and no coalesceable mutations
        tables.mutations.add_row(site=1, node=3, time=1, derived_state="G")
        tables.mutations.add_row(site=1, node=0, time=0, derived_state="T")
        tables.mutations.add_row(site=1, node=1, time=0, derived_state="A", parent=4)
        tables.mutations.add_row(site=1, node=2, time=0, derived_state="C", parent=4)

        ts = prepare(tables)

        ts2 = sc2ts.inference.coalesce_mutations(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 6
        assert ts2.num_nodes == 6


class TestPushUpReversions:
    def test_no_mutations(self):
        ts1 = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        ts2 = sc2ts.inference.push_up_reversions(ts1, [0, 1, 2, 3])
        ts1.tables.assert_equals(ts2.tables)

    def test_one_site_simple_reversion(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5   ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=4, time=1, derived_state="T")
        tables.mutations.add_row(site=0, node=3, time=0, derived_state="A")
        ts = prepare(tables)

        ts2 = sc2ts.inference.push_up_reversions(ts, [0, 1, 2, 3])
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == ts.num_mutations - 1
        assert ts2.num_nodes == ts.num_nodes + 1

    def test_one_site_simple_reversion_internal(self):
        # 4.00┊   8       ┊
        #     ┊ ┏━┻━┓     ┊
        # 3.00┊ ┃   7     ┊
        #     ┊ ┃ ┏━┻━┓   ┊
        # 2.00┊ ┃ ┃   6   ┊
        #     ┊ ┃ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃ ┃  5  ┊
        #     ┊ ┃ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 4 ┊
        #     0           1
        ts = tskit.Tree.generate_comb(5).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=6, time=2, derived_state="T")
        tables.mutations.add_row(site=0, node=5, time=1, derived_state="A")
        ts = prepare(tables)
        ts2 = sc2ts.inference.push_up_reversions(ts, [5])
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == ts.num_mutations - 1
        assert ts2.num_nodes == ts.num_nodes + 1

    def test_two_sites_reversion_and_shared(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5   ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.sites.add_row(0.5, "A")
        tables.mutations.add_row(site=0, node=4, time=1, derived_state="T")
        tables.mutations.add_row(site=0, node=3, time=0, derived_state="A")
        # Shared mutation over 4
        tables.mutations.add_row(site=1, node=4, time=1, derived_state="T")

        ts = prepare(tables)

        ts2 = sc2ts.inference.push_up_reversions(ts, [0, 1, 2, 3])
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == ts.num_mutations - 1
        assert ts2.num_nodes == ts.num_nodes + 1


class TestInsertRecombinants:
    def test_no_recombination(self):
        ts1 = tskit.Tree.generate_balanced(4, arity=4).tree_sequence
        ts2 = sc2ts.inference.insert_recombinants(ts1)
        ts1.tables.assert_equals(ts2.tables)

    def test_single_breakpoint_single_recombinant_no_mutations(self):
        tables = tskit.TableCollection(10)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=1, time=0)
        tables.edges.add_row(0, 5, parent=0, child=2)
        tables.edges.add_row(5, 10, parent=1, child=2)
        ts = prepare(tables)

        ts2 = sc2ts.inference.insert_recombinants(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 0
        assert ts2.num_nodes == ts.num_nodes + 1
        assert ts2.num_edges == ts.num_edges + 1
        assert_sequences_equal(ts, ts2)

    def test_single_breakpoint_two_recombinants_no_mutations(self):
        tables = tskit.TableCollection(10)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=1, time=0)
        tables.nodes.add_row(flags=1, time=0)
        tables.edges.add_row(0, 5, parent=0, child=2)
        tables.edges.add_row(5, 10, parent=1, child=2)
        tables.edges.add_row(0, 5, parent=0, child=3)
        tables.edges.add_row(5, 10, parent=1, child=3)
        ts = prepare(tables)

        ts2 = sc2ts.inference.insert_recombinants(ts)
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 0
        assert ts2.num_nodes == ts.num_nodes + 1
        assert ts2.num_edges == ts.num_edges
        assert_sequences_equal(ts, ts2)

    def test_single_breakpoint_single_recombinant_one_mutation(self):
        tables = tskit.TableCollection(10)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=1, time=0)
        tables.edges.add_row(0, 5, parent=0, child=2)
        tables.edges.add_row(5, 10, parent=1, child=2)
        tables.sites.add_row(4, "A")
        tables.mutations.add_row(site=0, node=2, derived_state="T")
        ts = prepare(tables)

        ts2 = sc2ts.inference.insert_recombinants(ts)
        md = ts2.node(3).metadata
        assert md["mutations"] == [[2, [[0, "A", "T"]]]]
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 1
        assert ts2.num_nodes == ts.num_nodes + 1
        assert ts2.num_edges == ts.num_edges + 1
        assert np.all(ts2.mutations_node == 3)

    def test_single_breakpoint_single_recombinant_two_mutations(self):
        tables = tskit.TableCollection(10)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=1, time=0)
        tables.edges.add_row(0, 5, parent=0, child=2)
        tables.edges.add_row(5, 10, parent=1, child=2)
        tables.sites.add_row(4, "A")
        tables.sites.add_row(5, "G")
        tables.mutations.add_row(site=0, node=2, derived_state="T")
        tables.mutations.add_row(site=1, node=2, derived_state="C")
        ts = prepare(tables)

        ts2 = sc2ts.inference.insert_recombinants(ts)
        md = ts2.node(3).metadata
        assert md["mutations"] == [[2, [[0, "A", "T"], [1, "G", "C"]]]]
        assert_sequences_equal(ts, ts2)
        assert ts2.num_mutations == 2
        assert ts2.num_nodes == ts.num_nodes + 1
        assert ts2.num_edges == ts.num_edges + 1
        assert np.all(ts2.mutations_node == 3)

    def test_single_breakpoint_two_recombinants_different_mutations(self):
        tables = tskit.TableCollection(10)
        tables.sites.add_row(4, "A")
        tables.sites.add_row(5, "G")
        tables.nodes.add_row(flags=0, time=1)
        tables.nodes.add_row(flags=0, time=1)
        for j in [2, 3]:
            tables.nodes.add_row(flags=1, time=0)
            tables.edges.add_row(0, 5, parent=0, child=j)
            tables.edges.add_row(5, 10, parent=1, child=j)
            # Share the mutation at site 0
            tables.mutations.add_row(site=0, node=j, derived_state="T")
        # Different mutations at site 1
        tables.mutations.add_row(site=1, node=2, derived_state="C")
        tables.mutations.add_row(site=1, node=3, derived_state="T")
        ts = prepare(tables)

        ts2 = sc2ts.inference.insert_recombinants(ts)
        assert_sequences_equal(ts, ts2)
        md = ts2.node(4).metadata
        assert ts2.num_mutations == 3
        assert ts2.num_nodes == ts.num_nodes + 1
        assert ts2.num_edges == ts.num_edges


class TestTrimBranches:
    def test_one_mutation_three_children(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5 x ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=5, derived_state="T")
        ts1 = tables.tree_sequence()

        ts2 = sc2ts.trim_branches(ts1)
        # 3.00┊   5     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   4   ┊
        #     ┊ ┃ ┏━╋━┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        assert ts2.num_trees == 1
        assert ts2.first().parent_dict == {0: 5, 1: 4, 2: 4, 3: 4, 4: 5}
        assert_variants_equal(ts1, ts2)

    def test_no_mutations(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5 x ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        ts1 = tables.tree_sequence()

        ts2 = sc2ts.trim_branches(ts1)
        assert ts2.num_trees == 1
        assert ts2.first().parent_dict == {0: 4, 1: 4, 2: 4, 3: 4}
        assert_variants_equal(ts1, ts2)

    def test_mutation_over_root(self):
        # 3.00┊   6 x   ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5   ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=6, derived_state="T")
        ts1 = tables.tree_sequence()

        ts2 = sc2ts.trim_branches(ts1)
        assert ts2.num_trees == 1
        assert ts2.first().parent_dict == {0: 4, 1: 4, 2: 4, 3: 4}
        assert_variants_equal(ts1, ts2)

    def test_one_leaf_mutation(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5   ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3x┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        tables.mutations.add_row(site=0, node=3, derived_state="T")
        ts1 = tables.tree_sequence()

        ts2 = sc2ts.trim_branches(ts1)
        # Tree is also flat because this mutation is private
        assert ts2.num_trees == 1
        assert ts2.first().parent_dict == {0: 4, 1: 4, 2: 4, 3: 4}
        assert_variants_equal(ts1, ts2)

    def test_n_leaf_mutations(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5   ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0x1x2x3x┊
        #     0         1
        ts = tskit.Tree.generate_comb(4).tree_sequence
        tables = ts.dump_tables()
        tables.sites.add_row(0, "A")
        for j in range(4):
            tables.mutations.add_row(site=0, node=j, derived_state="T")
        ts1 = tables.tree_sequence()

        ts2 = sc2ts.trim_branches(ts1)
        # Tree is also flat because all mutations are private
        assert ts2.num_trees == 1
        assert ts2.first().parent_dict == {0: 4, 1: 4, 2: 4, 3: 4}
        assert_variants_equal(ts1, ts2)

    def test_mutations_each_branch(self):
        # 3.00┊   6     ┊
        #     ┊ ┏━┻━┓   ┊
        # 2.00┊ ┃   5   ┊
        #     ┊ ┃ ┏━┻┓  ┊
        # 1.00┊ ┃ ┃  4  ┊
        #     ┊ ┃ ┃ ┏┻┓ ┊
        # 0.00┊ 0 1 2 3 ┊
        #     0         1
        ts = tskit.Tree.generate_comb(4, span=10).tree_sequence
        tables = ts.dump_tables()
        for j in range(6):
            tables.sites.add_row(j, "A")
            tables.mutations.add_row(site=j, node=j, derived_state="T")
        ts1 = tables.tree_sequence()

        ts2 = sc2ts.trim_branches(ts1)
        assert ts2.num_trees == 1
        assert ts2.first().parent_dict == ts1.first().parent_dict
        assert_variants_equal(ts1, ts2)

    @pytest.mark.parametrize("n", [2, 10, 100])
    @pytest.mark.parametrize("mutation_rate", [0.1, 0.5, 1.5])
    def test_simulation(self, n, mutation_rate):
        ts1 = msprime.sim_ancestry(n, sequence_length=100, ploidy=1, random_seed=3)
        ts1 = msprime.sim_mutations(ts1, rate=mutation_rate, random_seed=3234)
        ts2 = sc2ts.trim_branches(ts1)
        assert_variants_equal(ts1, ts2)


class TestInferBinary:
    @pytest.mark.parametrize("n", [2, 10, 15])
    @pytest.mark.parametrize("mutation_rate", [0.1, 0.5, 1.5])
    def test_simulation(self, n, mutation_rate):
        ts1 = msprime.sim_ancestry(n, sequence_length=100, ploidy=1, random_seed=3)
        ts1 = msprime.sim_mutations(ts1, rate=mutation_rate, random_seed=3234)
        ts2 = sc2ts.infer_binary(ts1)
        assert_variants_equal(ts1, ts2, allele_shuffle=True)
        assert ts2.num_trees == 1
        tree = ts2.first()
        assert tree.num_roots == 1
        for u in tree.nodes():
            assert len(tree.children(u)) in (0, 2)

    @pytest.mark.parametrize("n", [2, 10])
    @pytest.mark.parametrize("num_mutations", [1, 2, 10])
    def test_simulation_root_mutations(self, n, num_mutations):
        ts1 = msprime.sim_ancestry(n, sequence_length=100, ploidy=1, random_seed=3)
        root = ts1.first().root
        tables = ts1.dump_tables()
        for j in range(num_mutations):
            tables.sites.add_row(j, "A")
            tables.mutations.add_row(site=j, node=root, derived_state="T")
        ts1 = tables.tree_sequence()
        ts2 = sc2ts.infer_binary(ts1)
        assert_variants_equal(ts1, ts2)
        root = ts2.first().root
        assert np.all(ts2.mutations_node == root)
        assert ts2.num_trees == 1
        tree = ts2.first()
        assert tree.num_roots == 1
        for u in tree.nodes():
            assert len(tree.children(u)) in (0, 2)
