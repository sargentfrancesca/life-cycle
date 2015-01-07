-- phpMyAdmin SQL Dump
-- version 4.3.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 07, 2015 at 04:57 PM
-- Server version: 5.6.22
-- PHP Version: 5.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `lifecycle`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('3fc0efb94fd8');

-- --------------------------------------------------------

--
-- Table structure for table `coauthors`
--

CREATE TABLE IF NOT EXISTS `coauthors` (
  `user_name` varchar(64) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `coauthors`
--

INSERT INTO `coauthors` (`user_name`, `project_id`) VALUES
('Francesca Sargent', 1),
('Dave Hodgson', 1),
('Jennifer McDonald', 1),
('Francesca Sargent', 1),
('Dave Hodgson', 1),
('Dave Hodgson', 1),
('Jennifer McDonald', 1),
('Francesca Sargent', 1),
('Francesca Sargent', 1);

-- --------------------------------------------------------

--
-- Table structure for table `copubauthors`
--

CREATE TABLE IF NOT EXISTS `copubauthors` (
  `user_name` varchar(64) DEFAULT NULL,
  `publication_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `copubauthors`
--

INSERT INTO `copubauthors` (`user_name`, `publication_id`) VALUES
('Francesca Sargent', 1);

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE IF NOT EXISTS `projects` (
  `id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `urlname` varchar(100) DEFAULT NULL,
  `full_title` varchar(300) DEFAULT NULL,
  `brief_synopsis` text,
  `synopsis` text,
  `website` varchar(64) DEFAULT NULL,
  `twitter` varchar(64) DEFAULT NULL,
  `facebook` varchar(64) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `researcher_id` int(11) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`id`, `title`, `urlname`, `full_title`, `brief_synopsis`, `synopsis`, `website`, `twitter`, `facebook`, `timestamp`, `researcher_id`) VALUES
(1, 'Demography', 'demography', 'Are Structured Life Histories Really Buffered Against Environmental Change?', '', 'Proin eu lacinia enim. Curabitur pellentesque erat nisi, non porttitor lacus condimentum semper. Vestibulum quis est finibus, gravida justo eget, molestie tellus. Morbi et suscipit sem, nec scelerisque tellus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Duis ut ultricies risus, sit amet iaculis felis. Donec commodo vel dui id consectetur. Pellentesque ac felis condimentum, pulvinar nisl a, fringilla ex. Quisque sit amet ante eu sapien sagittis tincidunt sit amet accumsan est. Sed ac dolor non eros imperdiet tristique. Pellentesque aliquam, metus a placerat sodales, ligula odio iaculis quam, sit amet maximus velit augue sit amet metus.\r\n\r\nNunc non metus mattis, dignissim elit at, posuere sem. Fusce bibendum enim id mollis condimentum. Sed imperdiet commodo quam. Maecenas hendrerit enim sed est euismod interdum. Etiam eu fermentum tellus. Aenean in luctus justo. Sed ac turpis vel tellus mollis commodo et vitae purus. Morbi vehicula lacus eu elit ullamcorper egestas. Suspendisse egestas semper accumsan. Nullam suscipit rhoncus augue ut fermentum.\r\n\r\nNam tempor lorem sapien, at pharetra libero imperdiet at. Mauris porttitor, dolor vel ornare ullamcorper, nunc arcu blandit metus, vel volutpat magna libero id tortor. Nullam id metus cursus, efficitur enim id, elementum arcu. Cras quis sapien justo. Phasellus eget ligula facilisis, hendrerit ipsum non, efficitur tellus. Etiam a quam vitae elit vestibulum laoreet. Donec ac vestibulum quam. Phasellus ornare ex quis venenatis viverra. Nulla maximus lacus nisl, id tempus nibh blandit vitae. Nulla quam lectus, facilisis sit amet justo in, volutpat cursus diam.\r\n\r\nDonec blandit dui sed vestibulum hendrerit. Vivamus ornare nulla ac fringilla aliquam. Aenean scelerisque consectetur pharetra. Vivamus sit amet lectus arcu. Proin interdum vestibulum elit, nec euismod dui interdum dapibus. Praesent sollicitudin, neque mattis volutpat semper, est tortor ornare nulla, at tempus turpis nisl ac turpis. Phasellus eget rutrum nulla. Vestibulum elementum faucibus congue. Cras varius vitae nisi lacinia suscipit. Nam vel magna ut massa consequat imperdiet. Donec gravida, arcu a ultrices tempor, ligula velit fringilla massa, et sodales est lorem id neque. Phasellus molestie enim ac cursus facilisis. Duis iaculis est lectus, ac viverra augue volutpat quis. Nulla facilisi.\r\n\r\nNullam malesuada turpis eu dapibus ornare. Sed volutpat, enim sed interdum cursus, ex dolor finibus leo, ac bibendum ante dolor sed leo. Quisque eget scelerisque risus, id rutrum libero. Cras iaculis tempus purus, et ornare nulla congue quis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi sed tortor quis sem faucibus semper quis id purus. Pellentesque sem risus, aliquet eu felis et, posuere efficitur nulla.\r\n\r\nEtiam congue mauris lacus, sed pellentesque augue condimentum id. Curabitur aliquet et neque eu tristique. Cras ornare accumsan semper. Nam condimentum congue dui. Nam sit amet blandit eros, nec congue nisi. Sed volutpat a erat sit amet dignissim. Pellentesque fringilla nisl eu finibus facilisis. Ut dictum sed sapien vel lacinia. Quisque mollis, dolor vel lacinia interdum, sapien massa pulvinar mi, at fringilla justo lectus at lectus. Curabitur quis sollicitudin tellus. Nullam feugiat ex et arcu venenatis, eu aliquet lacus laoreet. Curabitur fringilla.', 'http://lifecycle.ex.ac.uk/demography', '', '', '2015-01-07 14:39:06', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `publications`
--

CREATE TABLE IF NOT EXISTS `publications` (
  `id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `urlname` varchar(100) DEFAULT NULL,
  `full_title` varchar(300) DEFAULT NULL,
  `brief_synopsis` text,
  `synopsis` text,
  `website` varchar(64) DEFAULT NULL,
  `twitter` varchar(64) DEFAULT NULL,
  `facebook` varchar(64) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `researcher_id` int(11) DEFAULT NULL,
  `project_id` varchar(100) DEFAULT NULL,
  `project_name` varchar(100) DEFAULT NULL,
  `citation` text
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `publications`
--

INSERT INTO `publications` (`id`, `title`, `urlname`, `full_title`, `brief_synopsis`, `synopsis`, `website`, `twitter`, `facebook`, `timestamp`, `researcher_id`, `project_id`, `project_name`, `citation`) VALUES
(1, 'Example', 'example', 'Lorem ipsum dolor sit amet.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam mauris risus, eleifend at arcu eu, bibendum porta sem. Ut dictum accumsan quam sit amet sodales. Duis non sapien sit amet quam porta dapibus. Morbi vehicula ut libero eu facilisis. Sed turpis eros, rhoncus sed felis sit amet, scelerisque imperdiet augue. Duis efficitur risus et consectetur sollicitudin. Integer tincidunt vehicula venenatis. Donec quis consequat mi, ac faucibus ante. Nullam et tempus nulla. Donec rutrum turpis in ligula ullamcorper mollis. Integer vel facilisis ipsum. Phasellus a libero ut libero molestie ultricies et quis ante. Ut imperdiet, nisl ut tincidunt sodales, ligula tellus.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vitae augue eu augue mattis aliquet eget et lorem. Nunc imperdiet augue nulla, at consequat enim vehicula sed. Suspendisse potenti. Sed convallis ligula vulputate mauris mattis sodales eget vel diam. Suspendisse dignissim augue vitae leo pharetra mollis. Nulla sit amet nisi luctus, posuere est ac, facilisis sapien. Sed mattis consectetur turpis, eget tristique mauris interdum in. Nullam tempor felis sed orci placerat, sed pulvinar augue lobortis. Fusce vel iaculis est, sit amet commodo nulla.\r\n\r\nMorbi efficitur nisi in nisl consectetur, eget gravida nibh aliquam. Nam et quam quam. Proin ipsum risus, venenatis at quam sit amet, porta viverra lorem. Nam aliquet diam eu fermentum finibus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer pellentesque nisi vel neque ornare, vel convallis nulla commodo. Maecenas lobortis massa ut odio mattis, id consequat dolor laoreet. Sed rhoncus augue non imperdiet vehicula. Donec in metus vitae neque egestas mattis. Nullam euismod rhoncus ex ut tempus. Nam vehicula risus volutpat semper scelerisque. Curabitur lobortis turpis at nisi ultricies maximus in vel augue. Fusce laoreet ante mollis lacinia tempus.\r\n\r\nNunc blandit, sem nec tempus ultricies, urna magna suscipit nisl, placerat laoreet mauris augue vitae velit. Sed mi turpis, varius at posuere mollis, ultrices sed augue. Mauris maximus condimentum magna ac varius. Nulla auctor, orci nec condimentum dapibus, ipsum elit luctus magna, sit amet interdum ante lorem pretium dolor. Nunc faucibus nunc vel laoreet tempus. Maecenas vel nunc pretium, fringilla arcu eu, sollicitudin ex. Curabitur vel fringilla metus, ac sollicitudin mi. Donec dapibus tortor elit, nec lacinia nulla tempor quis. Suspendisse vel arcu augue. Mauris sit amet nisl consequat, gravida nibh ac, dapibus diam.\r\n\r\nMaecenas diam mi, placerat sed nisl eget, finibus tincidunt dolor. Vestibulum quis bibendum ex. Sed non elementum elit. Vestibulum libero erat, consequat at lorem eu, pulvinar venenatis justo. Donec pellentesque magna ligula, et tincidunt neque rhoncus et. Suspendisse eleifend facilisis porta. Nam ac feugiat est, vel rutrum sem. Maecenas accumsan tellus id orci feugiat, elementum dictum risus suscipit. Vivamus in nulla tempus, tincidunt tortor vel, sagittis orci. Morbi blandit a nunc vitae posuere. Proin scelerisque auctor faucibus. Duis non varius arcu, at egestas enim. Aenean cursus, quam eget commodo molestie, sem nisl tempus neque, nec fringilla ligula ligula non neque. Sed non mollis nisl, sed convallis turpis. Integer quam sapien, convallis in metus id, consequat congue justo. Morbi lacus tortor, accumsan in tellus a, tempor condimentum ante.\r\n\r\nAliquam egestas vulputate vulputate. Ut vehicula scelerisque porttitor. Maecenas egestas sodales felis, nec posuere elit ultricies ac. Vestibulum ultrices pulvinar velit, sit amet blandit lectus egestas ac. Duis venenatis sem tellus, at vulputate ex tristique id. Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi sem neque, vulputate ac accumsan malesuada, congue et est. Nulla ullamcorper tincidunt mauris, ut iaculis ante commodo et. Morbi in egestas augue. Ut facilisis sit amet lorem nec posuere. Nam dictum vulputate commodo. Vivamus vitae elit finibus, tincidunt justo in, tristique mauris. Donec eget varius tortor, eget dignissim odio.', 'http://', NULL, NULL, '2015-01-07 16:34:37', NULL, NULL, 'demography', 'Holt, DH 1997, Management principles and practices, Prentice-Hall, Sydney.');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE IF NOT EXISTS `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `default` tinyint(1) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `default`, `permissions`) VALUES
(1, 'Moderator', 0, 15),
(2, 'Administrator', 1, 255),
(3, 'User', 0, 7);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL,
  `email` varchar(64) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `about_me` text,
  `quals` text,
  `jobtitle` varchar(64) DEFAULT NULL,
  `member_since` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `avatar_hash` varchar(32) DEFAULT NULL,
  `pub_email` varchar(64) DEFAULT NULL,
  `website` varchar(50) DEFAULT NULL,
  `twitter` varchar(64) DEFAULT NULL,
  `linkedin` varchar(64) DEFAULT NULL,
  `google` varchar(64) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `role_id`, `password_hash`, `confirmed`, `name`, `location`, `about_me`, `quals`, `jobtitle`, `member_since`, `last_seen`, `avatar_hash`, `pub_email`, `website`, `twitter`, `linkedin`, `google`) VALUES
(1, 'sargentfrancesca@gmail.com', 'francesca', 2, 'pbkdf2:sha1:1000$Q9VdYTBy$19ecc19f8e641b87ec045d88370dbfa19d94b38b', 1, 'Francesca Sargent', 'Falmouth', '~', '', 'Computing Development Officer', '2015-01-07 13:55:20', '2015-01-07 16:52:53', '1df2759f461f1039beb5c660e5acd109', 'f.sargent@exeter.ac.uk', 'http://chez.io', 'https://twitter.com/bellachezella', '', 'https://plus.google.com/u/0/101643196957978387971'),
(2, 'f.sargent@exeter.ac.uk', 'jenni', 2, 'pbkdf2:sha1:1000$lyHFLs43$542c9ceaabcb0a401ffb966447a4e9b588481617', 1, 'Jennifer McDonald', NULL, NULL, NULL, NULL, '2015-01-07 14:22:27', '2015-01-07 14:22:27', '966f533ba6bce3a0384b14a14a6324ce', NULL, NULL, NULL, NULL, NULL),
(3, 'bellachezella@gmail.com', 'dave', 2, 'pbkdf2:sha1:1000$iLXJiYdz$e9485d809e7a861c2f0fe8419ade613fc0a50c66', 1, 'Dave Hodgson', NULL, NULL, NULL, NULL, '2015-01-07 14:22:46', '2015-01-07 15:12:46', '0ef3596032aeb1c2e2a38214d79df891', NULL, NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `coauthors`
--
ALTER TABLE `coauthors`
  ADD KEY `project_id` (`project_id`), ADD KEY `user_name` (`user_name`);

--
-- Indexes for table `copubauthors`
--
ALTER TABLE `copubauthors`
  ADD KEY `publication_id` (`publication_id`), ADD KEY `user_name` (`user_name`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `urlname` (`urlname`), ADD KEY `researcher_id` (`researcher_id`), ADD KEY `ix_projects_timestamp` (`timestamp`);

--
-- Indexes for table `publications`
--
ALTER TABLE `publications`
  ADD PRIMARY KEY (`id`), ADD KEY `project_id` (`project_id`), ADD KEY `project_name` (`project_name`), ADD KEY `researcher_id` (`researcher_id`), ADD KEY `ix_publications_timestamp` (`timestamp`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`), ADD KEY `ix_roles_default` (`default`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`), ADD UNIQUE KEY `ix_users_email` (`email`), ADD UNIQUE KEY `ix_users_username` (`username`), ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `publications`
--
ALTER TABLE `publications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `coauthors`
--
ALTER TABLE `coauthors`
ADD CONSTRAINT `coauthors_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
ADD CONSTRAINT `coauthors_ibfk_2` FOREIGN KEY (`user_name`) REFERENCES `users` (`name`);

--
-- Constraints for table `copubauthors`
--
ALTER TABLE `copubauthors`
ADD CONSTRAINT `copubauthors_ibfk_1` FOREIGN KEY (`publication_id`) REFERENCES `publications` (`id`),
ADD CONSTRAINT `copubauthors_ibfk_2` FOREIGN KEY (`user_name`) REFERENCES `users` (`name`);

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`researcher_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `publications`
--
ALTER TABLE `publications`
ADD CONSTRAINT `publications_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `roles` (`name`),
ADD CONSTRAINT `publications_ibfk_2` FOREIGN KEY (`project_name`) REFERENCES `projects` (`urlname`),
ADD CONSTRAINT `publications_ibfk_3` FOREIGN KEY (`researcher_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
