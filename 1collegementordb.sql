-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 14, 2024 at 04:59 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1collegementordb`
--

-- --------------------------------------------------------

--
-- Table structure for table `mentortb`
--

CREATE TABLE `mentortb` (
  `id` bigint(50) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `Subject` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `mentortb`
--

INSERT INTO `mentortb` (`id`, `Name`, `Age`, `Mobile`, `Email`, `Address`, `Subject`, `UserName`, `Password`) VALUES
(4, 'sangeeth Kumar', '40', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'Python', 'san', 'san'),
(5, 'sangeeth Kumar', '23', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'Python', 'sangeeth', 'sangeeth'),
(6, 'ibbu', '46', '7904902206', 'sangeeth5535@gmail.com', 'No 16 samnath plaza, melapudur  trichy\r\nNo 16 samnath plaza, melapudur, trichy', 'Python', 'ibbu', 'ibbu');

-- --------------------------------------------------------

--
-- Table structure for table `querytb`
--

CREATE TABLE `querytb` (
  `id` bigint(10) NOT NULL auto_increment,
  `MName` varchar(250) NOT NULL,
  `Subject` varchar(500) NOT NULL,
  `Query` varchar(500) NOT NULL,
  `Answer` varchar(500) NOT NULL,
  `Date` date NOT NULL,
  `Sname` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `querytb`
--

INSERT INTO `querytb` (`id`, `MName`, `Subject`, `Query`, `Answer`, `Date`, `Sname`) VALUES
(2, 'sangeeth', 'Python', 'what is AI', 'hello', '2024-10-22', 'san1'),
(3, 'san', 'Python', 'what is list', 'list is python variable', '2024-11-02', 'ibbu');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(50) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Registerno` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `Batch` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Registerno`, `Mobile`, `Email`, `Address`, `Batch`, `UserName`, `Password`) VALUES
(4, 'sangeeth Kumar', '844101', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', '2020', 'san1', 'san1'),
(5, 'ibbu', '1009', '7904902206', 'sangeeth5535@gmail.com', 'No 16 samnath plaza, melapudur  trichy\r\nNo 16 samnath plaza, melapudur, trichy', '2022', 'ibbu', 'ibbu');

-- --------------------------------------------------------

--
-- Table structure for table `sharetb`
--

CREATE TABLE `sharetb` (
  `id` bigint(20) NOT NULL auto_increment,
  `MName` varchar(250) NOT NULL,
  `Subject` varchar(250) NOT NULL,
  `Document` varchar(500) NOT NULL,
  `Info` varchar(500) NOT NULL,
  `Batch` varchar(250) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `sharetb`
--

INSERT INTO `sharetb` (`id`, `MName`, `Subject`, `Document`, `Info`, `Batch`, `Date`) VALUES
(1, 'san', 'Python', '81641tamilmv77.txt', 'Nill', '2020', '2024-10-21'),
(2, 'ibbu', 'Python', '4512123.docx', 'python basics', '2022', '2024-11-02');
