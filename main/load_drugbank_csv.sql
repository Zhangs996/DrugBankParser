CREATE TABLE `drugbank05_drugs` (
  `drugbank_id` varchar(255) NOT NULL DEFAULT '',
  `drugname` varchar(255) NOT NULL DEFAULT '',
  `drug_type` varchar(255) NOT NULL DEFAULT '',
  `approved` int(1) NOT NULL,
  `experimental` int(1) NOT NULL,
  `illicit` int(1) NOT NULL,
  `investigational` int(1) NOT NULL,
  `nutraceutical` int(1) NOT NULL,
  `withdrawn` int(1) NOT NULL,
  PRIMARY KEY (`drugbank_id`),
  KEY `drug_type` (`drug_type`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

load data local infile 'drugbank05_drugs.csv'
into table drugbank05_drugs
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;



CREATE TABLE `drugbank05_drug2target` (
  `drugbank_id` varchar(255) NOT NULL DEFAULT '',
  `partner_id` varchar(255) NOT NULL DEFAULT '',
  `inhibitor` int(1) NOT NULL,
  `antagonist` int(1) NOT NULL,
  `agonist` int(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

load data local infile 'drugbank05_drug2target.csv'
into table drugbank05_drug2target
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;



CREATE TABLE `drugbank05_drug2enzyme` (
  `drugbank_id` varchar(255) NOT NULL DEFAULT '',
  `partner_id` varchar(255) NOT NULL DEFAULT '',
  `substrate` int(1) NOT NULL,
  `inducer` int(1) NOT NULL,
  `inhibitor` int(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

load data local infile 'drugbank05_drug2enzyme.csv'
into table drugbank05_drug2enzyme
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;



CREATE TABLE `drugbank05_drug2transporter` (
  `drugbank_id` varchar(255) NOT NULL DEFAULT '',
  `partner_id` varchar(255) NOT NULL DEFAULT '',
  `substrate` int(1) NOT NULL,
  `inducer` int(1) NOT NULL,
  `inhibitor` int(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

load data local infile 'drugbank05_drug2transporter.csv'
into table drugbank05_drug2transporter
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;



CREATE TABLE `drugbank05_partner_protein` (
  `partner_id` varchar(255) NOT NULL DEFAULT '',
  `partner_name` varchar(255) NOT NULL DEFAULT '',
  `gene_name` varchar(255) NOT NULL DEFAULT '',
  `uniprot_id` varchar(255) NOT NULL DEFAULT '',
  `genbank_gene_id` varchar(255) NOT NULL DEFAULT '',
  `genbank_protein_id` varchar(255) NOT NULL DEFAULT '',
  `hgnc_id` varchar(255) NOT NULL DEFAULT '',
  `organism` varchar(255) NOT NULL DEFAULT '',
  `taxonomy_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

load data local infile 'drugbank05_partner_protein.csv'
into table drugbank05_partner_protein
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;