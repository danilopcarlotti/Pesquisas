CREATE DATABASE `jurisprudencia_carf` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `jurisprudencia_carf`;

CREATE TABLE `decisoes_carf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acordao` varchar(450) DEFAULT NULL,
  `numero_processo` varchar(450) DEFAULT NULL,
  `data_publicacao` varchar(45) DEFAULT NULL,
  `contribuinte` varchar(450) DEFAULT NULL,
  `relator` varchar(450) DEFAULT NULL,
  `ementa` text,
  `decisao` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `html_decisoes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `html_decisoes` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
