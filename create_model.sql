-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema cs_go_bi
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema csgo_stats_dw
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema csgo_stats_dw
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `csgo_stats_dw` ;
USE `csgo_stats_dw` ;

-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`event` (
  `id` INT NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `region` VARCHAR(45) NULL,
  `tier` INT NULL,
  `stars` DECIMAL(3,3) NULL,
  `lan` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`de_map`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`de_map` (
  `id` INT NOT NULL,
  `name` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`match`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`match` (
  `id` INT NOT NULL,
  `best_of` INT NOT NULL,
  `tier` INT NULL,
  `stars` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`player` (
  `id` INT NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `country` VARCHAR(64) NOT NULL,
  `age` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`team` (
  `id` INT NOT NULL,
  `name` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`time` (
  `id` INT NOT NULL,
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  `day` INT NOT NULL,
  `semester` INT NULL DEFAULT NULL,
  `quarter` INT NULL DEFAULT NULL,
  `week_of_month` INT NULL DEFAULT NULL,
  `weekday` INT NULL,
  `weekend` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`performance_fact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`performance_fact` (
  `event_id` INT NOT NULL,
  `match_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `time_id` INT NOT NULL,
  `kills` INT NOT NULL,
  `deaths` INT NOT NULL,
  `assists` INT NOT NULL,
  `headshots` INT NOT NULL,
  `kddiff` INT NOT NULL,
  `fkdiff` INT NOT NULL,
  `adr` FLOAT NOT NULL,
  `kast` FLOAT NOT NULL,
  `rating` FLOAT NOT NULL,
  PRIMARY KEY (`event_id`, `match_id`, `team_id`, `player_id`),
  INDEX `fk_player_performance_fact_team1_idx` (`team_id` ASC) VISIBLE,
  INDEX `fk_player_performance_fact_match1_idx` (`match_id` ASC) VISIBLE,
  INDEX `fk_player_performance_fact_event1_idx` (`event_id` ASC) VISIBLE,
  INDEX `fk_player_performance_fact_player1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_player_performance_fact_time1_idx` (`time_id` ASC) VISIBLE,
  CONSTRAINT `fk_player_performance_fact_event1`
    FOREIGN KEY (`event_id`)
    REFERENCES `csgo_stats_dw`.`event` (`id`),
  CONSTRAINT `fk_player_performance_fact_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `csgo_stats_dw`.`match` (`id`),
  CONSTRAINT `fk_player_performance_fact_player1`
    FOREIGN KEY (`player_id`)
    REFERENCES `csgo_stats_dw`.`player` (`id`),
  CONSTRAINT `fk_player_performance_fact_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `csgo_stats_dw`.`team` (`id`),
  CONSTRAINT `fk_player_performance_fact_time1`
    FOREIGN KEY (`time_id`)
    REFERENCES `csgo_stats_dw`.`time` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `csgo_stats_dw`.`vetoes_fact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `csgo_stats_dw`.`vetoes_fact` (
  `event_id` INT NOT NULL,
  `match_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `de_map_id` INT NOT NULL,
  `time_id` INT NOT NULL,
  `number` INT NOT NULL,
  PRIMARY KEY (`event_id`, `match_id`, `team_id`, `de_map_id`),
  INDEX `fk_vetoes_fact_match1_idx` (`match_id` ASC) VISIBLE,
  INDEX `fk_vetoes_fact_team1_idx` (`team_id` ASC) VISIBLE,
  INDEX `fk_vetoes_fact_de_map1_idx` (`de_map_id` ASC) VISIBLE,
  INDEX `fk_vetoes_fact_time1_idx` (`time_id` ASC) VISIBLE,
  CONSTRAINT `fk_vetoes_fact_event1`
    FOREIGN KEY (`event_id`)
    REFERENCES `csgo_stats_dw`.`event` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vetoes_fact_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `csgo_stats_dw`.`match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vetoes_fact_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `csgo_stats_dw`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vetoes_fact_de_map1`
    FOREIGN KEY (`de_map_id`)
    REFERENCES `csgo_stats_dw`.`de_map` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vetoes_fact_time1`
    FOREIGN KEY (`time_id`)
    REFERENCES `csgo_stats_dw`.`time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
