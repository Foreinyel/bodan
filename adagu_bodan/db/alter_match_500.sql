ALTER TABLE `soccer_data`.`match_500` ADD `predict_win_no_win` smallint(2) NULL COMMENT '预测胜/不胜:1/0';
ALTER TABLE `soccer_data`.`match_500` ADD `ouzhi_odds_aomen` DECIMAL(8,3) NULL COMMENT '欧指澳门';
ALTER TABLE `soccer_data`.`match_500` ADD `profit` DECIMAL(10,4) NULL COMMENT '单场收益';


ALTER TABLE `soccer_data`.`match_500` ADD `ouzhi_odds_best` DECIMAL(8,3) NULL COMMENT '最佳欧指';
ALTER TABLE `soccer_data`.`match_500` ADD `profit_best` DECIMAL(10,4) NULL COMMENT '最佳单场收益';