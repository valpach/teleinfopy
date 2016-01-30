-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 20, 2016 at 04:11 PM
-- Server version: 5.5.40
-- PHP Version: 5.4.36-0+deb7u1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `teleinfo`
--

-- --------------------------------------------------------

--
-- Table structure for table `teleinfo`
--

CREATE TABLE IF NOT EXISTS `teleinfo` (
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ADCO` varchar(12) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL COMMENT 'Adresse du compteur',
  `OPTARIF` varchar(4) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL COMMENT 'Option tarifaire choisie ',
  `ISOUSC` varchar(2) NOT NULL COMMENT 'Intensité souscrite (A)',
  `BASE` varchar(9) NOT NULL COMMENT 'option Base (Wh)',
  `HCHC` varchar(9) NOT NULL COMMENT 'Heures Creuses (Wh)',
  `HCHP` varchar(9) NOT NULL COMMENT 'Heures Pleines (Wh)',
  `EJPHN` varchar(9) NOT NULL COMMENT 'EJP Heures Normales (Wh)',
  `EJPHPM` varchar(9) NOT NULL COMMENT 'EJP Heures de Pointe (Wh)',
  `BBRHCJB` varchar(9) NOT NULL COMMENT 'Tempo HC Jours Bleus (Wh)',
  `BBRHPJB` varchar(9) NOT NULL COMMENT 'Tempo HP Jours Bleus (Wh)',
  `BBRHCJW` varchar(9) NOT NULL COMMENT 'Tempo HC Jours Blancs (Wh)',
  `BBRHPJW` varchar(9) NOT NULL COMMENT 'Tempo HP Jours Blancs (Wh)',
  `BBRHCJR` varchar(9) NOT NULL COMMENT 'Tempo HC Jours Rouges (Wh)',
  `BBRHPJR` varchar(9) NOT NULL COMMENT 'Tempo HP Jours Rouges (Wh)',
  `PEJP` varchar(2) NOT NULL COMMENT 'Préavis Début EJP (mn)',
  `PTEC` varchar(4) NOT NULL COMMENT 'Période Tarifaire en cours',
  `DEMAIN` varchar(4) NOT NULL COMMENT 'Couleur du lendemain',
  `IINST1` varchar(3) NOT NULL COMMENT 'Intensité Instantanée phase 1',
  `IINST2` varchar(3) NOT NULL COMMENT 'Intensité Instantanée phase 2',
  `IINST3` varchar(3) NOT NULL COMMENT 'Intensité Instantanée phase 3',
  `IMAX1` varchar(3) NOT NULL COMMENT 'Intensité maximale phase 1',
  `IMAX2` varchar(3) NOT NULL COMMENT 'Intensité maximale phase 2',
  `IMAX3` varchar(3) NOT NULL COMMENT 'Intensité maximale phase 3',
  `PMAX` varchar(5) NOT NULL COMMENT 'Puissance maximale triphasée atteinte ',
  `PAPP` varchar(5) NOT NULL COMMENT 'Puissance apparente triphasée',
  `HHPHC` varchar(1) NOT NULL COMMENT 'Horaire Heures Pleines Heures Creuses',
  `MOTDETAT` varchar(6) NOT NULL COMMENT 'Mot d''Etat du compteur',
  `PPOT` varchar(2) NOT NULL COMMENT 'Présence des potentiels',
  PRIMARY KEY (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
