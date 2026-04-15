-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema utstyrsutleiedb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema utstyrsutleiedb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `utstyrsutleiedb` DEFAULT CHARACTER SET utf8 ;
USE `utstyrsutleiedb` ;

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`PostSted`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`PostSted` (
  `PostNr` CHAR(4) NOT NULL,
  `PostSted` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`PostNr`),
  UNIQUE INDEX `PostNr_UNIQUE` (`PostNr` ASC) )
ENGINE = InnoDB;

INSERT INTO `poststed` VALUES ('8000','Bodø'),('8001','Bodø'),('8500','Narvik'),('8501','Narvik'),('9000','Tromsø'),('9001','Tromsø');

-- -----------------------------------------------------
-- Table `UtstyrsUtleiedb`.`AdresseType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`AdresseType` (
  `AdresseTypeID` INT NOT NULL,
  `Beskrivelse` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`AdresseTypeID`))
ENGINE = InnoDB;

INSERT INTO `AdresseType` VALUES (1,'Faktura'),(2,'Levering');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Adresse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Adresse` (
  `AdresseId` INT NOT NULL,
  `AdresseTypeID` INT NOT NULL,
  `PostNr` CHAR(4) NOT NULL,
  `AdrGate` VARCHAR(100) NOT NULL,
  `AdrGateNr` INT NOT NULL,
  INDEX `fk_Adress_Postnr1_idx` (`PostNr` ASC) ,
  PRIMARY KEY (`AdresseId`),
  INDEX `fk_Adresse_AdresseType1_idx` (`AdresseTypeID` ASC) ,
  CONSTRAINT `fk_Adress_Postnr100`
    FOREIGN KEY (`PostNr`)
    REFERENCES `utstyrsutleiedb`.`PostSted` (`PostNr`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Adresse_AdresseType1`
    FOREIGN KEY (`AdresseTypeID`)
    REFERENCES `utstyrsutleiedb`.`AdresseType` (`AdresseTypeID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `Adresse` VALUES (1,'2','9000','Murergata',2),(3,'2','8000','Lillegata',233),(5,'2','8000','Veien',124),(7,'2','8500','Fjelltoppen',3),(2,'1','9001','Murergata',1),(4,'1','8001','Øvregata',332),(6,'1','8000','Nedreveien',223),(8,'1','8501','Fjelltoppen',4);

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Kunde`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Kunde` (
  `KundeNr` INT NOT NULL,
  `KundeEpost` VARCHAR(45) NOT NULL,
  `Fakt_AdresseId` INT NOT NULL,
  `Levering_AdresseId` INT NOT NULL,
  PRIMARY KEY (`KundeNr`),
  INDEX `fk_Kunde_Adresse2_idx` (`Fakt_AdresseId` ASC) ,
  INDEX `fk_Kunde_Adresse1_idx` (`Levering_AdresseId` ASC) ,
  CONSTRAINT `fk_Kunde_Adresse2`
    FOREIGN KEY (`Fakt_AdresseId`)
    REFERENCES `utstyrsutleiedb`.`Adresse` (`AdresseId`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Kunde_Adresse1`
    FOREIGN KEY (`Levering_AdresseId`)
    REFERENCES `utstyrsutleiedb`.`Adresse` (`AdresseId`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `Kunde` VALUES (8988,'mu_pe@ånnlain.no','2','1'),(10002,'gm@uuiitt.nu','4','3'),(11122,'lok_bygg@no.no','6','5'),(20011,'aa@post.no','8','7');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`PrivatKunde`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`PrivatKunde` (
  `KundeNr` INT NOT NULL,
  `Fornavn` VARCHAR(45) NOT NULL,
  `Etternavn` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`KundeNr`),
  CONSTRAINT `fk_PrivatKunde_Kunde1`
    FOREIGN KEY (`KundeNr`)
    REFERENCES `utstyrsutleiedb`.`Kunde` (`KundeNr`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `Privatkunde` VALUES (20011,'Anders','Andersen');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`KundeTelefon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`KundeTelefon` (
  `KundeNr` INT NOT NULL,
  `TelefonNr` CHAR(8) NOT NULL,
  PRIMARY KEY (`KundeNr`, `TelefonNr`),
  INDEX `fk_KundeTelefon_Kunde1_idx` (`KundeNr` ASC) ,
  CONSTRAINT `fk_KundeTelefon_Kunde1`
    FOREIGN KEY (`KundeNr`)
    REFERENCES `utstyrsutleiedb`.`Kunde` (`KundeNr`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `Kundetelefon` VALUES (8988,90099888),(10002,76900111),(10002,99988877),(11122,70766554),(20011,22122333),(20011,76900112),(20011,99988777);

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Kundebehandler`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Kundebehandler` (
  `KundebehandlerId` INT NOT NULL,
  `Fornavn` VARCHAR(45) NOT NULL,
  `Etternavn` VARCHAR(45) NOT NULL,
  `TelefonNr` CHAR(8) NOT NULL,
  PRIMARY KEY (`KundebehandlerId`))
ENGINE = InnoDB;

INSERT INTO `kundebehandler` VALUES (1,'Hilde ','Pettersen ','10090999'),(2,'Berit','Hansen ','10191999'),(3,'Hans','Hansen ','10291999');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`UtstyrsKategori`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`UtstyrsKategori` (
  `UtstyrsKatId` INT NOT NULL,
  `Beskrivelse` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`UtstyrsKatId`))
ENGINE = InnoDB;

INSERT INTO `Utstyrskategori` VALUES (1,'Lette maskiner'),(2,'Tunge maskiner'),(3,'Annleggsutstyr');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Utstyr`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Utstyr` (
  `UtstyrId` INT NOT NULL,
  `UtstyrsType` VARCHAR(45) NOT NULL,
  `UtstyrsMerke` VARCHAR(45) NOT NULL,
  `UtstyrsModell` VARCHAR(45) NOT NULL,
  `Beskrivelse` VARCHAR(250) NULL,
  `UtstyrsKatId` INT NOT NULL,
  `LeiePrisDøgn` DECIMAL(10,2) NOT NULL,
  `AntallUtstyr` INT NOT NULL,
  `AntallPåLager` INT NULL,
  PRIMARY KEY (`UtstyrId`),
  INDEX `fk_Utstyr_UtstyrsKategori1_idx` (`UtstyrsKatId` ASC) ,
  CONSTRAINT `fk_Utstyr_UtstyrsKategori1`
    FOREIGN KEY (`UtstyrsKatId`)
    REFERENCES `utstyrsutleiedb`.`UtstyrsKategori` (`UtstyrsKatId`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `Utstyr` VALUES (233,'Kompressor','Stanley','Vento 6L','Liten og hendig, med en motor på 1,5HK. Regulerbart trykk opp till 8bar, 180L luft i minuttet. ',1,79,10,4),(234,'Spikerpistol','ESSVE','Coil CN-15-65','ESSVE Coilpistol beregnet for spikring av bjelkelag, reisverk, kledning, utforinger, panel, sponplater m.m. Smidig spikerpistol med maskinkropp i magnesium, justerbart utblås og beltekrok.',1,100,50,45),(1001,'Minigraver','Hitachi','ZX10U-6','Minigraveren ZX10U-6 fra Hitachi er vår minste minigraver og er laget for bruk på trange og små plasser',2,1200,1,0),(7653,'Stilas','Haki Stilas','150','Stilas på ca 150 kvadratmeter.',3,350,2,1),(7654,'Sementblander','Atika','130l 600w','Atika betongblander med kapasitet på 130 l og 600 W. Bruker 230 V. IP44',3,230,8,4);

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Instans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Instans` (
  `Instansid` INT NOT NULL,
  `UtstyrId` INT NOT NULL,
  `Sistevedlikehold` DATE NOT NULL,
  `Nestevedlikehold` DATE NOT NULL,
  PRIMARY KEY (`Instansid`, `UtstyrId`),
  INDEX `fk_Instans_Utstyr1_idx` (`UtstyrId` ASC) ,
  CONSTRAINT `fk_Instans_Utstyr10`
    FOREIGN KEY (`UtstyrId`)
    REFERENCES `utstyrsutleiedb`.`Utstyr` (`UtstyrId`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `Instans` VALUES (1,233,'2018-04-03','2021-04-03'),(1,234,'2021-02-10','2022-02-10'),(1,1001,'2019-09-01','2022-09-01'),(1,7653,'2016-12-11','2021-12-11'),(1,7654,'2019-03-20','2024-03-20'),(2,233,'2017-01-02','2022-01-02');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Betalingsmåte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Betalingsmåte` (
  `BetalingsmåteId` INT NOT NULL,
  `Beskrivelse` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`BetalingsmåteId`))
ENGINE = InnoDB;

INSERT INTO `betalingsmåte` VALUES (1,'Kontant'),(2,'Kort'),(3,'Vips');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`Utleie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`Utleie` (
  `UtleieId` INT NOT NULL AUTO_INCREMENT,
  `UtstyrId` INT NOT NULL,
  `Instansid` INT NOT NULL,
  `KundeNr` INT NOT NULL,
  `UtleidDato` DATE NOT NULL,
  `InnlevertDato` DATE NULL,
  `KundebehandlerId` INT NOT NULL,
  `Levereskunde` VARCHAR(3) NOT NULL,
  `BetalingsmåteId` INT NOT NULL,
  `Leveringskostnad` DECIMAL(10,2) NULL,
  `Totalpris` DECIMAL(10,2) NULL,
  PRIMARY KEY (`UtleieId`),
  INDEX `fk_Utleie_Kundebehandler1_idx` (`KundebehandlerId` ASC) ,
  INDEX `fk_Utleie_Instans1_idx` (`Instansid` ASC, `UtstyrId` ASC) ,
  INDEX `fk_Utleie_Kunde2_idx` (`KundeNr` ASC) ,
  INDEX `fk_Utleie_Betalingsmåte1_idx` (`BetalingsmåteId` ASC) ,
  CONSTRAINT `fk_Utleie_Kundebehandler10`
    FOREIGN KEY (`KundebehandlerId`)
    REFERENCES `utstyrsutleiedb`.`Kundebehandler` (`KundebehandlerId`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Utleie_Instans10`
    FOREIGN KEY (`Instansid` , `UtstyrId`)
    REFERENCES `utstyrsutleiedb`.`Instans` (`Instansid` , `UtstyrId`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Utleie_Kunde2`
    FOREIGN KEY (`KundeNr`)
    REFERENCES `utstyrsutleiedb`.`Kunde` (`KundeNr`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_Utleie_Betalingsmåte1`
    FOREIGN KEY (`BetalingsmåteId`)
    REFERENCES `utstyrsutleiedb`.`Betalingsmåte` (`BetalingsmåteId`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
    CONSTRAINT UC_Utleie UNIQUE ( KundeNr, Instansid, UtstyrId, UtleidDato )
    )
ENGINE = InnoDB;

INSERT INTO `Utleie` VALUES (1,234, 1, 11122, '2019-02-01','2019-02-03', 3,'Nei',2,0,200),(2,233, 2, 20011,'2019-03-05','2019-03-06', 2,'Nei',1,0,79),(3,7654, 1, 8988,'2020-02-04','2020-02-10', 2,'Ja',3,200,1580),(4,233, 1,20011,'2021-02-01',NULL, 1,'Ja',2,150,NULL),(5,1001, 1, 10002, '2021-02-05','2021-02-08', 1,'Ja',1,500,4100),(6,7653, 1, 11122,'2021-02-05',NULL, 2,'Nei',2,0,NULL);

-- -----------------------------------------------------
-- Table `UtstyrsUtleiedb`.`BedriftKunde`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`.`BedriftKunde` (
  `KundeNr` INT NOT NULL,
  `Kundenavn` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`KundeNr`),
  CONSTRAINT `fk_BedriftKunde_Kunde1`
    FOREIGN KEY (`KundeNr`)
    REFERENCES `utstyrsutleiedb`.`Kunde` (`KundeNr`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

INSERT INTO `bedriftkunde` VALUES (8988,'Murer Pedersen ANS'),(10002,'Grøft og Kant AS'),(11122,'Lokalbyggern AS');

-- -----------------------------------------------------
-- Table `utstyrsutleiedb`.`user`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `utstyrsutleiedb`. `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fornavn` varchar(100) NOT NULL,
  `etternavn` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB;

INSERT INTO `user` VALUES (1,'Hilde ','Pettersen','hildep@utstyr.no','scrypt:32768:8:1$yGgUAlfW2UCqizI1$0288b7d8c58da998908b839c62c29922b09b565efbec3b11b5a73dc45159465ef735289b3ad1c27420cd87f5b8926853cb5777b7cbeb1c76c45ce48c8e56f39b','user','2026-04-12 20:25:44'),(2,'Berit ','Hansen','berith@utstyr.no','scrypt:32768:8:1$krq8L3XxpjO1OE8F$835881b3f9c2411516922f930eadbb6c926e45f491b9eceb90b16ddb7dc055d2246530aef1978eece3c816dfa14a3ee15b2372caaeb4205c7b81e837188f9737','user','2026-04-12 20:26:34'),(3,'Hans ','Hansen','hansh@utstyr.no','scrypt:32768:8:1$9IYxfOdPdaM9iTT4$b360e703b9c96ede3a853d2554c7c96a861ad9634fd93ced2ddbc53177a6b40c71d4d12658116a3d232c7b2b78161a34163b6ad6a32772bcc4e05dbec754246c','user','2026-04-12 20:27:13'),(11,'Test','test','test@epost.com','scrypt:32768:8:1$shYtWx1F79pBzZy2$42efbbc99f3d4d3c20cca3ae15824b8d6551cc85708a47575f06589cea1340175092e71a1ca074b321b4ffd5e53025cc691f74bb2c52bc9e8c3eb44c32764528','user','2026-04-14 09:15:47');



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
