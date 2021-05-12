-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bi_csgo
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bi_csgo
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bi_csgo` ;
USE `bi_csgo` ;

-- -----------------------------------------------------
-- Table `bi_csgo`.`event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`event` (
  `id` INT NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `lan` TINYINT NULL,
  `tier` INT NULL,
  `stars` DECIMAL(3,3) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`map`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`map` (
  `id` INT NOT NULL,
  `name` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`match`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`match` (
  `id` INT NOT NULL,
  `best_of` INT NOT NULL,
  `tier` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`player` (
  `id` INT NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `country` VARCHAR(64) NOT NULL,
  `region` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`team` (
  `id` INT NOT NULL,
  `name` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`time` (
  `id` INT NOT NULL,
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  `day` INT NOT NULL,
  `semester` INT NOT NULL,
  `quarter` INT NOT NULL,
  `week_of_month` INT NOT NULL,
  `weekday` INT NOT NULL,
  `weekend` TINYINT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`performance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`performance` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `kills` INT NOT NULL,
  `deaths` INT NOT NULL,
  `assists` INT NOT NULL,
  `hs` INT NOT NULL,
  `kd_diff` INT NOT NULL,
  `fk_diff` INT NOT NULL,
  `adr` DOUBLE NOT NULL,
  `kast` DOUBLE NOT NULL,
  `rating` DOUBLE NOT NULL,
  `event_id` INT NOT NULL,
  `match_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `time_id` INT NOT NULL,
  INDEX `fk_performance_fact_event1_idx` (`event_id` ASC) VISIBLE,
  INDEX `fk_performance_fact_match1_idx` (`match_id` ASC) VISIBLE,
  INDEX `fk_performance_fact_player1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_performance_fact_team1_idx` (`team_id` ASC) VISIBLE,
  INDEX `fk_performance_fact_time1_idx` (`time_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_performance_fact_event1`
    FOREIGN KEY (`event_id`)
    REFERENCES `bi_csgo`.`event` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_performance_fact_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `bi_csgo`.`match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_performance_fact_player1`
    FOREIGN KEY (`player_id`)
    REFERENCES `bi_csgo`.`player` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_performance_fact_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `bi_csgo`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_performance_fact_time1`
    FOREIGN KEY (`time_id`)
    REFERENCES `bi_csgo`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bi_csgo`.`veto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bi_csgo`.`veto` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `event_id` INT NOT NULL,
  `match_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `map_id` INT NOT NULL,
  `time_id` INT NOT NULL,
  `number` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_veto_fact_event_idx` (`event_id` ASC) VISIBLE,
  INDEX `fk_veto_fact_match1_idx` (`match_id` ASC) VISIBLE,
  INDEX `fk_veto_fact_team1_idx` (`team_id` ASC) VISIBLE,
  INDEX `fk_veto_fact_map1_idx` (`map_id` ASC) VISIBLE,
  INDEX `fk_veto_fact_time1_idx` (`time_id` ASC) VISIBLE,
  CONSTRAINT `fk_veto_fact_event`
    FOREIGN KEY (`event_id`)
    REFERENCES `bi_csgo`.`event` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_veto_fact_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `bi_csgo`.`match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_veto_fact_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `bi_csgo`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_veto_fact_map1`
    FOREIGN KEY (`map_id`)
    REFERENCES `bi_csgo`.`map` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_veto_fact_time1`
    FOREIGN KEY (`time_id`)
    REFERENCES `bi_csgo`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
