-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: utstyrsutleiedb
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '336102b3-efa9-11f0-8734-9cda3e867675:1-336,
8d484176-ec89-11f0-9c75-4ccc6add35f6:1-189,
c39c862c-31a1-11f1-9800-9082c340a2b7:1-47,
cd8c833a-f055-11f0-bc3c-ad3c23fe8fd3:1-1379';

--
-- Create database with correct name
--

CREATE DATABASE utstyrsutleiedb;

--
-- Table structure for table `adresse`
--

DROP TABLE IF EXISTS `adresse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adresse` (
  `AdresseId` int NOT NULL,
  `AdresseTypeID` int NOT NULL,
  `PostNr` char(4) NOT NULL,
  `AdrGate` varchar(100) NOT NULL,
  `AdrGateNr` int NOT NULL,
  PRIMARY KEY (`AdresseId`),
  KEY `fk_Adress_Postnr1_idx` (`PostNr`),
  KEY `fk_Adresse_AdresseType1_idx` (`AdresseTypeID`),
  CONSTRAINT `fk_Adress_Postnr100` FOREIGN KEY (`PostNr`) REFERENCES `poststed` (`PostNr`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_Adresse_AdresseType1` FOREIGN KEY (`AdresseTypeID`) REFERENCES `adressetype` (`AdresseTypeID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adresse`
--

LOCK TABLES `adresse` WRITE;
/*!40000 ALTER TABLE `adresse` DISABLE KEYS */;
INSERT INTO `adresse` VALUES (1,2,'9000','Murergata',2),(2,1,'9001','Murergata',1),(3,2,'8000','Lillegata',233),(4,1,'8001','Øvregata',332),(5,2,'8000','Veien',124),(6,1,'8000','Nedreveien',223),(7,2,'8500','Fjelltoppen',3),(8,1,'8501','Fjelltoppen',4);
/*!40000 ALTER TABLE `adresse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adressetype`
--

DROP TABLE IF EXISTS `adressetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adressetype` (
  `AdresseTypeID` int NOT NULL,
  `Beskrivelse` varchar(45) NOT NULL,
  PRIMARY KEY (`AdresseTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adressetype`
--

LOCK TABLES `adressetype` WRITE;
/*!40000 ALTER TABLE `adressetype` DISABLE KEYS */;
INSERT INTO `adressetype` VALUES (1,'Faktura'),(2,'Levering');
/*!40000 ALTER TABLE `adressetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bedriftkunde`
--

DROP TABLE IF EXISTS `bedriftkunde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bedriftkunde` (
  `KundeNr` int NOT NULL,
  `Kundenavn` varchar(45) NOT NULL,
  PRIMARY KEY (`KundeNr`),
  CONSTRAINT `fk_BedriftKunde_Kunde1` FOREIGN KEY (`KundeNr`) REFERENCES `kunde` (`KundeNr`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bedriftkunde`
--

LOCK TABLES `bedriftkunde` WRITE;
/*!40000 ALTER TABLE `bedriftkunde` DISABLE KEYS */;
INSERT INTO `bedriftkunde` VALUES (8988,'Murer Pedersen ANS'),(10002,'Grøft og Kant AS'),(11122,'Lokalbyggern AS');
/*!40000 ALTER TABLE `bedriftkunde` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `betalingsmåte`
--

DROP TABLE IF EXISTS `betalingsmåte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `betalingsmåte` (
  `BetalingsmåteId` int NOT NULL,
  `Beskrivelse` varchar(45) NOT NULL,
  PRIMARY KEY (`BetalingsmåteId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `betalingsmåte`
--

LOCK TABLES `betalingsmåte` WRITE;
/*!40000 ALTER TABLE `betalingsmåte` DISABLE KEYS */;
INSERT INTO `betalingsmåte` VALUES (1,'Kontant'),(2,'Kort'),(3,'Vips');
/*!40000 ALTER TABLE `betalingsmåte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instans`
--

DROP TABLE IF EXISTS `instans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instans` (
  `Instansid` int NOT NULL,
  `UtstyrId` int NOT NULL,
  `Sistevedlikehold` date NOT NULL,
  `Nestevedlikehold` date NOT NULL,
  PRIMARY KEY (`Instansid`,`UtstyrId`),
  KEY `fk_Instans_Utstyr1_idx` (`UtstyrId`),
  CONSTRAINT `fk_Instans_Utstyr10` FOREIGN KEY (`UtstyrId`) REFERENCES `utstyr` (`UtstyrId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instans`
--

LOCK TABLES `instans` WRITE;
/*!40000 ALTER TABLE `instans` DISABLE KEYS */;
INSERT INTO `instans` VALUES (1,233,'2018-04-03','2021-04-03'),(1,234,'2021-02-10','2022-02-10'),(1,1001,'2019-09-01','2022-09-01'),(1,7653,'2016-12-11','2021-12-11'),(1,7654,'2019-03-20','2024-03-20'),(2,233,'2017-01-02','2022-01-02');
/*!40000 ALTER TABLE `instans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kunde`
--

DROP TABLE IF EXISTS `kunde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kunde` (
  `KundeNr` int NOT NULL,
  `KundeEpost` varchar(45) NOT NULL,
  `Fakt_AdresseId` int NOT NULL,
  `Levering_AdresseId` int NOT NULL,
  PRIMARY KEY (`KundeNr`),
  KEY `fk_Kunde_Adresse2_idx` (`Fakt_AdresseId`),
  KEY `fk_Kunde_Adresse1_idx` (`Levering_AdresseId`),
  CONSTRAINT `fk_Kunde_Adresse1` FOREIGN KEY (`Levering_AdresseId`) REFERENCES `adresse` (`AdresseId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_Kunde_Adresse2` FOREIGN KEY (`Fakt_AdresseId`) REFERENCES `adresse` (`AdresseId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kunde`
--

LOCK TABLES `kunde` WRITE;
/*!40000 ALTER TABLE `kunde` DISABLE KEYS */;
INSERT INTO `kunde` VALUES (8988,'mu_pe@ånnlain.no',2,1),(10002,'gm@uuiitt.nu',4,3),(11122,'lok_bygg@no.no',6,5),(20011,'aa@post.no',8,7);
/*!40000 ALTER TABLE `kunde` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kundebehandler`
--

DROP TABLE IF EXISTS `kundebehandler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kundebehandler` (
  `KundebehandlerId` int NOT NULL,
  `Fornavn` varchar(45) NOT NULL,
  `Etternavn` varchar(45) NOT NULL,
  `TelefonNr` char(8) DEFAULT NULL,
  PRIMARY KEY (`KundebehandlerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kundebehandler`
--

LOCK TABLES `kundebehandler` WRITE;
/*!40000 ALTER TABLE `kundebehandler` DISABLE KEYS */;
INSERT INTO `kundebehandler` VALUES (1,'Hilde ','Pettersen ','10090999'),(2,'Berit','Hansen ','10191999'),(3,'Hans','Hansen ','10291999'),(11,'Test','test',NULL);
/*!40000 ALTER TABLE `kundebehandler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kundetelefon`
--

DROP TABLE IF EXISTS `kundetelefon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kundetelefon` (
  `KundeNr` int NOT NULL,
  `TelefonNr` char(8) NOT NULL,
  PRIMARY KEY (`KundeNr`,`TelefonNr`),
  KEY `fk_KundeTelefon_Kunde1_idx` (`KundeNr`),
  CONSTRAINT `fk_KundeTelefon_Kunde1` FOREIGN KEY (`KundeNr`) REFERENCES `kunde` (`KundeNr`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kundetelefon`
--

LOCK TABLES `kundetelefon` WRITE;
/*!40000 ALTER TABLE `kundetelefon` DISABLE KEYS */;
INSERT INTO `kundetelefon` VALUES (8988,'90099888'),(10002,'76900111'),(10002,'99988877'),(11122,'70766554'),(20011,'22122333'),(20011,'76900112'),(20011,'99988777');
/*!40000 ALTER TABLE `kundetelefon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `poststed`
--

DROP TABLE IF EXISTS `poststed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `poststed` (
  `PostNr` char(4) NOT NULL,
  `PostSted` varchar(45) NOT NULL,
  PRIMARY KEY (`PostNr`),
  UNIQUE KEY `PostNr_UNIQUE` (`PostNr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `poststed`
--

LOCK TABLES `poststed` WRITE;
/*!40000 ALTER TABLE `poststed` DISABLE KEYS */;
INSERT INTO `poststed` VALUES ('8000','Bodø'),('8001','Bodø'),('8500','Narvik'),('8501','Narvik'),('9000','Tromsø'),('9001','Tromsø');
/*!40000 ALTER TABLE `poststed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `privatkunde`
--

DROP TABLE IF EXISTS `privatkunde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `privatkunde` (
  `KundeNr` int NOT NULL,
  `Fornavn` varchar(45) NOT NULL,
  `Etternavn` varchar(45) NOT NULL,
  PRIMARY KEY (`KundeNr`),
  CONSTRAINT `fk_PrivatKunde_Kunde1` FOREIGN KEY (`KundeNr`) REFERENCES `kunde` (`KundeNr`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `privatkunde`
--

LOCK TABLES `privatkunde` WRITE;
/*!40000 ALTER TABLE `privatkunde` DISABLE KEYS */;
INSERT INTO `privatkunde` VALUES (20011,'Anders','Andersen');
/*!40000 ALTER TABLE `privatkunde` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fornavn` varchar(100) NOT NULL,
  `etternavn` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Hilde ','Pettersen','hildep@utstyr.no','scrypt:32768:8:1$yGgUAlfW2UCqizI1$0288b7d8c58da998908b839c62c29922b09b565efbec3b11b5a73dc45159465ef735289b3ad1c27420cd87f5b8926853cb5777b7cbeb1c76c45ce48c8e56f39b','user','2026-04-12 20:25:44'),(2,'Berit ','Hansen','berith@utstyr.no','scrypt:32768:8:1$krq8L3XxpjO1OE8F$835881b3f9c2411516922f930eadbb6c926e45f491b9eceb90b16ddb7dc055d2246530aef1978eece3c816dfa14a3ee15b2372caaeb4205c7b81e837188f9737','user','2026-04-12 20:26:34'),(3,'Hans ','Hansen','hansh@utstyr.no','scrypt:32768:8:1$9IYxfOdPdaM9iTT4$b360e703b9c96ede3a853d2554c7c96a861ad9634fd93ced2ddbc53177a6b40c71d4d12658116a3d232c7b2b78161a34163b6ad6a32772bcc4e05dbec754246c','user','2026-04-12 20:27:13'),(11,'Test','test','test@epost.com','scrypt:32768:8:1$shYtWx1F79pBzZy2$42efbbc99f3d4d3c20cca3ae15824b8d6551cc85708a47575f06589cea1340175092e71a1ca074b321b4ffd5e53025cc691f74bb2c52bc9e8c3eb44c32764528','user','2026-04-14 09:15:47');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utleie`
--

DROP TABLE IF EXISTS `utleie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utleie` (
  `UtleieId` int NOT NULL AUTO_INCREMENT,
  `UtstyrId` int NOT NULL,
  `Instansid` int NOT NULL,
  `KundeNr` int NOT NULL,
  `UtleidDato` date NOT NULL,
  `InnlevertDato` date DEFAULT NULL,
  `KundebehandlerId` int NOT NULL,
  `Levereskunde` varchar(3) NOT NULL,
  `BetalingsmåteId` int NOT NULL,
  `Leveringskostnad` decimal(10,2) DEFAULT NULL,
  `Totalpris` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`UtleieId`),
  KEY `fk_Utleie_Kundebehandler1_idx` (`KundebehandlerId`),
  KEY `fk_Utleie_Instans1_idx` (`Instansid`,`UtstyrId`),
  KEY `fk_Utleie_Kunde2_idx` (`KundeNr`),
  KEY `fk_Utleie_Betalingsmåte1_idx` (`BetalingsmåteId`),
  CONSTRAINT `fk_Utleie_Betalingsmåte1` FOREIGN KEY (`BetalingsmåteId`) REFERENCES `betalingsmåte` (`BetalingsmåteId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_Utleie_Instans10` FOREIGN KEY (`Instansid`, `UtstyrId`) REFERENCES `instans` (`Instansid`, `UtstyrId`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_Utleie_Kunde2` FOREIGN KEY (`KundeNr`) REFERENCES `kunde` (`KundeNr`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_Utleie_Kundebehandler10` FOREIGN KEY (`KundebehandlerId`) REFERENCES `kundebehandler` (`KundebehandlerId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utleie`
--

LOCK TABLES `utleie` WRITE;
/*!40000 ALTER TABLE `utleie` DISABLE KEYS */;
INSERT INTO `utleie` VALUES (1,234,1,11122,'2019-02-01','2019-02-03',3,'Nei',2,0.00,200.00),(2,233,2,20011,'2019-03-05','2019-03-06',2,'Nei',1,0.00,79.00),(3,7654,1,8988,'2020-02-04','2020-02-10',2,'Ja',3,200.00,1580.00),(4,233,1,20011,'2021-02-01',NULL,1,'Ja',2,150.00,NULL),(5,1001,1,10002,'2021-02-05','2021-02-08',1,'Ja',1,500.00,4100.00),(6,7653,1,11122,'2021-02-05',NULL,2,'Nei',2,0.00,NULL),(7,234,1,10002,'2026-04-14','2026-04-14',1,'Nei',2,NULL,NULL),(8,233,2,8988,'2026-04-17','2026-04-14',1,'Nei',2,NULL,NULL),(10,233,2,8988,'2026-04-14',NULL,11,'Ja',1,NULL,NULL);
/*!40000 ALTER TABLE `utleie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utstyr`
--

DROP TABLE IF EXISTS `utstyr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utstyr` (
  `UtstyrId` int NOT NULL,
  `UtstyrsType` varchar(45) NOT NULL,
  `UtstyrsMerke` varchar(45) NOT NULL,
  `UtstyrsModell` varchar(45) NOT NULL,
  `Beskrivelse` varchar(250) DEFAULT NULL,
  `UtstyrsKatId` int NOT NULL,
  `LeiePrisDøgn` decimal(10,2) NOT NULL,
  `AntallUtstyr` int NOT NULL,
  `AntallPåLager` int DEFAULT NULL,
  PRIMARY KEY (`UtstyrId`),
  KEY `fk_Utstyr_UtstyrsKategori1_idx` (`UtstyrsKatId`),
  CONSTRAINT `fk_Utstyr_UtstyrsKategori1` FOREIGN KEY (`UtstyrsKatId`) REFERENCES `utstyrskategori` (`UtstyrsKatId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utstyr`
--

LOCK TABLES `utstyr` WRITE;
/*!40000 ALTER TABLE `utstyr` DISABLE KEYS */;
INSERT INTO `utstyr` VALUES (233,'Kompressor','Stanley','Vento 6L','Liten og hendig, med en motor på 1,5HK. Regulerbart trykk opp till 8bar, 180L luft i minuttet. ',1,79.00,10,4),(234,'Spikerpistol','ESSVE','Coil CN-15-65','ESSVE Coilpistol beregnet for spikring av bjelkelag, reisverk, kledning, utforinger, panel, sponplater m.m. Smidig spikerpistol med maskinkropp i magnesium, justerbart utblås og beltekrok.',1,100.00,50,45),(1001,'Minigraver','Hitachi','ZX10U-6','Minigraveren ZX10U-6 fra Hitachi er vår minste minigraver og er laget for bruk på trange og små plasser',2,1200.00,1,0),(7653,'Stilas','Haki Stilas','150','Stilas på ca 150 kvadratmeter.',3,350.00,2,1),(7654,'Sementblander','Atika','130l 600w','Atika betongblander med kapasitet på 130 l og 600 W. Bruker 230 V. IP44',3,230.00,8,4);
/*!40000 ALTER TABLE `utstyr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utstyrskategori`
--

DROP TABLE IF EXISTS `utstyrskategori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utstyrskategori` (
  `UtstyrsKatId` int NOT NULL,
  `Beskrivelse` varchar(50) NOT NULL,
  PRIMARY KEY (`UtstyrsKatId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utstyrskategori`
--

LOCK TABLES `utstyrskategori` WRITE;
/*!40000 ALTER TABLE `utstyrskategori` DISABLE KEYS */;
INSERT INTO `utstyrskategori` VALUES (1,'Lette maskiner'),(2,'Tunge maskiner'),(3,'Annleggsutstyr');
/*!40000 ALTER TABLE `utstyrskategori` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-14 11:54:37
