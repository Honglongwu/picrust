#!/usr/bin/env python
# File created on 22 Feb 2012
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011-2013, The PICRUSt Project"
__credits__ = ["Greg Caporaso","Jesse Zaneveld"]
__license__ = "GPL"
__version__ = "0.9.1-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"
 

from cogent.util.unit_test import TestCase, main
from biom.parse import parse_biom_table_str, get_axis_indices,\
  direct_slice_data
from biom.table import DenseTable
from picrust.predict_metagenomes import predict_metagenomes,\
  calc_nsti,get_overlapping_ids,\
  extract_otu_and_genome_data,transfer_sample_metadata,\
  transfer_observation_metadata,transfer_metadata,\
  load_subset_from_biom_str,yield_subset_biom_str

class PredictMetagenomeTests(TestCase):
    """ """
    
    def setUp(self):
        self.otu_table1 = parse_biom_table_str(otu_table1)
        self.otu_table1_with_metadata = parse_biom_table_str(otu_table1_with_metadata)
        self.genome_table1 = parse_biom_table_str(genome_table1)
        self.genome_table1_with_metadata = parse_biom_table_str(genome_table1_with_metadata)
        self.genome_table2 = parse_biom_table_str(genome_table2)
        self.predicted_metagenome_table1 = parse_biom_table_str(predicted_metagenome_table1)
        self.predicted_metagenome_table1_with_metadata = parse_biom_table_str(predicted_metagenome_table1_with_metadata)
 
    def test_predict_metagenomes(self):
        """ predict_metagenomes functions as expected with valid input """
        actual = predict_metagenomes(self.otu_table1,self.genome_table1)
        self.assertEqual(actual,self.predicted_metagenome_table1)

    def test_predict_metagenomes_value_error(self):
        """ predict_metagenomes raises ValueError when no overlapping otu ids """
        self.assertRaises(ValueError,predict_metagenomes,self.otu_table1,self.genome_table2)

    def test_predict_metagenomes_keeps_observation_metadata(self):
        """predict_metagenomes preserves Observation metadata in genome and otu table"""
        
        actual = predict_metagenomes(self.otu_table1_with_metadata,self.genome_table1_with_metadata)
        exp = self.predicted_metagenome_table1_with_metadata
        
        #Need to map to dicts, otherwise the memory location of the lambda function
        #associated with the defaultdict causes (artifactual) inequality of results
        
        actual_md = map(dict,sorted([md for md in actual.ObservationMetadata]))
        exp_md = map(dict,sorted([md for md in exp.ObservationMetadata]))
        for i,md in enumerate(actual_md):
            self.assertEqualItems(md,exp_md[i])
        for i,md in enumerate(exp_md):
            self.assertEqualItems(md,actual_md[i])

    def test_predict_metagenomes_keeps_sample_metadata(self):
        """predict_metagenomes preserves Sample metadata in genome and otu table"""
        #NOTE: could be consolidated with "_keeps_observation_metadata above

        actual = predict_metagenomes(self.otu_table1_with_metadata,\
          self.genome_table1_with_metadata,verbose=False)
        exp = self.predicted_metagenome_table1_with_metadata
        
        #Need to map to dicts, otherwise the memory location of the lambda function
        #associated with the defaultdict causes (artifactual) inequality of results
        
        actual_md = map(dict,sorted([md for md in actual.SampleMetadata]))
        exp_md = map(dict,sorted([md for md in exp.SampleMetadata]))
        for i,md in enumerate(actual_md):
            self.assertEqualItems(md,exp_md[i])
        for i,md in enumerate(exp_md):
            self.assertEqualItems(md,actual_md[i])

    def test_transfer_metadata_moves_sample_metadata_between_biom_tables(self):
        """transfer_metadata moves sample metadata values between BIOM format tables"""
        t1 = self.otu_table1
        exp = self.otu_table1_with_metadata
        actual = transfer_metadata(self.otu_table1_with_metadata,self.otu_table1,\
          "SampleMetadata","SampleMetadata",verbose=False)
        
        actual_md = map(dict,sorted([md for md in actual.SampleMetadata]))
        exp_md = map(dict,sorted([md for md in exp.SampleMetadata]))
        for i,md in enumerate(actual_md):
            self.assertEqualItems(md,exp_md[i])
        for i,md in enumerate(exp_md):
            self.assertEqualItems(md,actual_md[i])
    
    def test_transfer_metadata_moves_observation_metadata_between_biom_tables(self):
        """transfer_metadata moves observation metadata values between BIOM format tables"""
        t1 = self.genome_table1
        exp = self.genome_table1_with_metadata
        actual = transfer_metadata(self.genome_table1_with_metadata,\
          self.genome_table1,"ObservationMetadata","ObservationMetadata",verbose=False)
        
        actual_md = map(dict,sorted([md for md in actual.ObservationMetadata]))
        exp_md = map(dict,sorted([md for md in exp.ObservationMetadata]))
        for i,md in enumerate(actual_md):
            self.assertEqualItems(md,exp_md[i])
        for i,md in enumerate(exp_md):
            self.assertEqualItems(md,actual_md[i])


    def test_transfer_sample_metadata_moves_sample_metadata_between_biom_tables(self):
        """transfer_sample_metadata moves sample metadata values between BIOM format tables"""
        t1 = self.otu_table1
        exp = self.otu_table1_with_metadata
        actual = transfer_sample_metadata(self.otu_table1_with_metadata,\
          self.otu_table1,"SampleMetadata",verbose=False)
        
        actual_md = map(dict,sorted([md for md in actual.SampleMetadata]))
        exp_md = map(dict,sorted([md for md in exp.SampleMetadata]))
        for i,md in enumerate(actual_md):
            self.assertEqualItems(md,exp_md[i])
        for i,md in enumerate(exp_md):
            self.assertEqualItems(md,actual_md[i])

    def test_transfer_observation_metadata_moves_observation_metadata_between_biom_tables(self):
        """transfer_sample_metadata moves sample metadata values between BIOM format tables"""
        t1 = self.genome_table1
        exp = self.genome_table1_with_metadata
        actual = transfer_observation_metadata(self.genome_table1_with_metadata,\
          self.genome_table1,"ObservationMetadata",verbose=False)
        
        actual_md = map(dict,sorted([md for md in actual.ObservationMetadata]))
        exp_md = map(dict,sorted([md for md in exp.ObservationMetadata]))
        for i,md in enumerate(actual_md):
            self.assertEqualItems(md,exp_md[i])
        for i,md in enumerate(exp_md):
            self.assertEqualItems(md,actual_md[i])

    def test_load_subset_from_biom_str_loads_a_subset_of_observations(self):
        """load_subset_from_biom_str loads a subset of observations from a valid BIOM format JSON string"""
        biom_str = otu_table1_with_metadata
        ids_to_load = ['GG_OTU_1','GG_OTU_2']
        axis = 'observations'
        #NOTE: this will fail currently due to a known bug in the BIOM direct_parse_key
        #as soon as that is updated this should pass, however
        #two_taxon_table = load_subset_from_biom_str(biom_str,ids_to_load,axis)
        #self.assertEqualItems(two_taxon_table.ObservationIds,ids_to_load)
        
        #Test that loading all ids is identical to just loading the table
        #exp = parse_biom(biom_str)
        #obs = load_subset_from_biom_str(biom_str,ids_to_load=['GG_OTU_1','GG_OTU_2','GG_OTU_3'],axis=axis)
        #self.assertEqual(obs,exp)

    def test_yield_subset_biom_str_yields_string_pieces_from_valid_input(self):
        """yield_subset_biom_str yields components of a biom string containing only a subset of ids, given a valid biom str"""
        biom_str = otu_table1_with_metadata
        ids_to_load = ['GG_OTU_1','GG_OTU_2']
        axis = 'observations'
        
        idxs, new_axis_md = get_axis_indices(biom_str,ids_to_load, axis)
        new_data = direct_slice_data(biom_str,idxs, axis)

        #NOTE: this will fail currently due to a known bug in the BIOM direct_parse_key
        #as soon as that is updated this should pass, however
        obs = [part for part in yield_subset_biom_str(biom_str,new_data,new_axis_md,axis)]
        exp = ['{', '"id": "GG_OTU_1"', ',',\
                '"format": "Biological Observation Matrix v0.9"', ',',\
                '"format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html"', ',',\
                '"type": "OTU table"', ',',\
#                '"generated_by": "QIIME 1.4.0-dev, svn revision 2753', ',',\
                '"generated_by": "QIIME 1.4.0-dev', ',',\
                '"date": "2012-02-22T20:50:05.024661"', ',',\
                '"matrix_type": "sparse"', ',',\
                '"matrix_element_type": "float"', ',',\
                '"data": [[0,0,1.0],[0,1,2.0],[0,2,3.0],[0,3,5.0],[1,0,5.0],[1,1,1.0],[1,3,2.0]], "shape": [2, 4]',',',\
                '"rows": [{"id": "GG_OTU_1", "metadata": null}, {"id": "GG_OTU_2", "metadata": null}]', ',',\
                '"columns": [{"id": "Sample1", "metadata": {"pH":7.0}}, {"id": "Sample2", "metadata": {"pH":8.0}}, {"id": "Sample3", "metadata": {"pH":7.0}}, {"id": "Sample4", "metadata": null}]', '}']
        #For now be aware that commas in generated_by
        #strings won't parse correnctly 
        for i,piece in enumerate(exp):
            self.assertEqual(obs[i],piece)
        #TODO: when BIOM direct_parse_key is fixed this should pass
        #self.assertEqual(obs,exp)


otu_table1 = """{"rows": [{"id": "GG_OTU_1", "metadata": null}, {"id": "GG_OTU_2", "metadata": null}, {"id": "GG_OTU_3", "metadata": null}], "format": "Biological Observation Matrix v0.9", "data": [[0, 0, 1.0], [0, 1, 2.0], [0, 2, 3.0], [0, 3, 5.0], [1, 0, 5.0], [1, 1, 1.0], [1, 3, 2.0], [2, 2, 1.0], [2, 3, 4.0]], "columns": [{"id": "Sample1", "metadata": null}, {"id": "Sample2", "metadata": null}, {"id": "Sample3", "metadata": null}, {"id": "Sample4", "metadata": null}], "generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 4], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T20:50:05.024661", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

otu_table1_with_metadata = """{"rows": [{"id": "GG_OTU_1", "metadata": null}, {"id": "GG_OTU_2", "metadata": null}, {"id": "GG_OTU_3", "metadata": null}], "format": "Biological Observation Matrix v0.9", "data": [[0, 0, 1.0], [0, 1, 2.0], [0, 2, 3.0], [0, 3, 5.0], [1, 0, 5.0], [1, 1, 1.0], [1, 3, 2.0], [2, 2, 1.0], [2, 3, 4.0]], "columns": [{"id": "Sample1", "metadata": {"pH":7.0}}, {"id": "Sample2", "metadata": {"pH":8.0}}, {"id": "Sample3", "metadata": {"pH":7.0}}, {"id": "Sample4", "metadata": null}],"generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 4], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T20:50:05.024661", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

genome_table1 = """{"rows": [{"id": "f1", "metadata": null}, {"id": "f2", "metadata": null}, {"id": "f3", "metadata": null}], "format": "Biological Observation Matrix v0.9", "data": [[0, 0, 1.0], [0, 1, 2.0], [0, 2, 3.0], [1, 1, 1.0], [2, 2, 1.0]], "columns": [{"id": "GG_OTU_1", "metadata": null}, {"id": "GG_OTU_3", "metadata": null}, {"id": "GG_OTU_2", "metadata": null}], "generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 3], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T20:49:58.258296", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

genome_table1_with_metadata = """{"rows": [{"id": "f1", "metadata": {"KEGG_description":"ko00100    Steroid biosynthesis"}}, {"id": "f2", "metadata": {"KEGG_description":"ko00195   Photosynthesis"}}, {"id": "f3", "metadata": {"KEGG_description":"ko00232    Caffeine metabolism"}}], "format": "Biological Observation Matrix v0.9", "data": [[0, 0, 1.0], [0, 1, 2.0], [0, 2, 3.0], [1, 1, 1.0], [2, 2, 1.0]], "columns": [{"id": "GG_OTU_1", "metadata": {"confidence": 0.665,"taxonomy": ["Root", "k__Bacteria", "p__Firmicutes", "c__Clostridia", "o__Clostridiales", "f__Lachnospiraceae"]}}, {"id": "GG_OTU_3", "metadata": {"confidence": 1.0,"taxonomy": ["Root", "k__Bacteria", "p__Firmicutes", "c__Clostridia", "o__Clostridiales", "f__Lachnospiraceae"]}}, {"id": "GG_OTU_2", "metadata":{"confidence": 0.98,"taxonomy": ["Root", "k__Bacteria"]}}], "generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 3], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T20:49:58.258296", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

genome_table2 = """{"rows": [{"id": "f1", "metadata": null}, {"id": "f2", "metadata": null}, {"id": "f3", "metadata": null}], "format": "Biological Observation Matrix v0.9", "data": [[0, 0, 1.0], [0, 1, 2.0], [0, 2, 3.0], [1, 1, 1.0], [2, 2, 1.0]], "columns": [{"id": "GG_OTU_21", "metadata": null}, {"id": "GG_OTU_23", "metadata": null}, {"id": "GG_OTU_22", "metadata": null}], "generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 3], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T20:49:58.258296", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

predicted_metagenome_table1 = """{"rows": [{"id": "f1", "metadata": null}, {"id": "f2", "metadata": null}, {"id": "f3", "metadata": null}], "format": "Biological Observation Matrix v0.9", "data": [[0, 0, 16.0], [0, 1, 5.0], [0, 2, 5.0], [0, 3, 19.0], [1, 2, 1.0], [1, 3, 4.0], [2, 0, 5.0], [2, 1, 1.0], [2, 3, 2.0]], "columns": [{"id": "Sample1", "metadata": null}, {"id": "Sample2", "metadata": null}, {"id": "Sample3", "metadata": null}, {"id": "Sample4", "metadata": null}], "generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 4], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T16:01:30.837052", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

predicted_metagenome_table1_with_metadata = """{"rows": [{"id": "f1", "metadata": {"KEGG_description":"ko00100    Steroid biosynthesis"}}, {"id": "f2", "metadata": {"KEGG_description":"ko00195   Photosynthesis"}}, {"id": "f3", "metadata": {"KEGG_description":"ko00232    Caffeine metabolism"}}], "format": "Biological Observation Matrix v0.9","data": [[0, 0, 16.0], [0, 1, 5.0], [0, 2, 5.0], [0, 3, 19.0], [1, 2, 1.0], [1, 3, 4.0], [2, 0, 5.0], [2, 1, 1.0], [2, 3, 2.0]], "columns": [{"id": "Sample1", "metadata": {"pH":7.0}}, {"id": "Sample2", "metadata": {"pH":8.0}}, {"id": "Sample3", "metadata": {"pH":7.0}}, {"id": "Sample4", "metadata": null}], "generated_by": "QIIME 1.4.0-dev, svn revision 2753", "matrix_type": "sparse", "shape": [3, 4], "format_url": "http://www.qiime.org/svn_documentation/documentation/biom_format.html", "date": "2012-02-22T16:01:30.837052", "type": "OTU table", "id": null, "matrix_element_type": "float"}"""

if __name__ == "__main__":
    main()
