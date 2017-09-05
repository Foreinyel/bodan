USE `soccer_data` ;

-- -----------------------------------------------------
-- Table `soccer_data`.`bodan_500`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`bodan_500` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`bodan_500` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `league` VARCHAR(45) NOT NULL COMMENT '',
  `start_time` DATETIME NOT NULL COMMENT '',
  `home` VARCHAR(45) NULL COMMENT '',
  `away` VARCHAR(45) NULL COMMENT '',
  `home_goal` SMALLINT(5) NULL ,
  `away_goal` SMALLINT(5) NULL ,
  `odds_comp` VARCHAR(45) null,
  `one_zero` VARCHAR(45) NULL ,
  `two_zero` VARCHAR(45) NULL ,
  `two_one` VARCHAR(45) NULL ,
  `three_zero` VARCHAR(45) NULL ,
  `three_one` VARCHAR(45) NULL ,
  `three_two` VARCHAR(45) null,
  `four_zero` VARCHAR(45) null,
  `four_one` VARCHAR(45) null,
  `four_two` VARCHAR(45) null,
  `four_three` VARCHAR(45) null,
  `zero_one` VARCHAR(45) null,
  `zero_two` VARCHAR(45) null,
  `one_two` VARCHAR(45) null,
  `zero_three` VARCHAR(45) null,
  `one_three` VARCHAR(45) null,
  `two_three` VARCHAR(45) null,
  `zero_four` VARCHAR(45) null,
  `one_four` VARCHAR(45) null,
  `two_four` VARCHAR(45) null,
  `three_four` VARCHAR(45) null,
  `zero_zero` VARCHAR(45) null,
  `one_one` VARCHAR(45) null,
  `two_two` VARCHAR(45) null,
  `three_three` VARCHAR(45) null,
  `four_four` VARCHAR(45) null,
  `returns` VARCHAR(45) null,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

ALTER TABLE `soccer_data`.`bodan_500` ADD `hit_standing` SMALLINT(2) NULL COMMENT '命中排名';
ALTER TABLE `soccer_data`.`bodan_500` ADD `lowest_odds` DECIMAL(10,4) NULL COMMENT '最低赔率';
ALTER TABLE `soccer_data`.`bodan_500` ADD `hit_odds` DECIMAL(10,4) NULL COMMENT '命中赔率';
ALTER TABLE `soccer_data`.`bodan_500` ADD `profit` DECIMAL(10,4) NULL COMMENT '单场收益';
ALTER TABLE `soccer_data`.`bodan_500` ADD `win_or_lose` smallint(2) NULL COMMENT '胜平负';
ALTER TABLE `soccer_data`.`bodan_500` ADD `win_no_win` smallint(2) NULL COMMENT '胜/不胜:1/0';
ALTER TABLE `soccer_data`.`bodan_500` ADD `predict_win_no_win` smallint(2) NULL COMMENT '预测胜/不胜:1/0';
ALTER TABLE `soccer_data`.`bodan_500` ADD `win_no_win_profit` DECIMAL(10,4) NULL COMMENT 'win_no_win单场收益';
ALTER TABLE `soccer_data`.`bodan_500` ADD `win_no_win_cost` DECIMAL(10,4) NULL COMMENT 'win_no_win单场成本';
