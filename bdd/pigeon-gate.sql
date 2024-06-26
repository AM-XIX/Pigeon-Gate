-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : mer. 26 juin 2024 à 13:56
-- Version du serveur : 5.7.39
-- Version de PHP : 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `pigeon-gate`
--

-- --------------------------------------------------------

--
-- Structure de la table `Categorie`
--

CREATE TABLE `Categorie` (
  `idCat` int(255) NOT NULL,
  `nom` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `Categorie`
--

INSERT INTO `Categorie` (`idCat`, `nom`) VALUES
(1, 'Estropié'),
(2, 'Pride'),
(3, 'Punk');

-- --------------------------------------------------------

--
-- Structure de la table `Categorise`
--

CREATE TABLE `Categorise` (
  `idLinkCat` int(255) NOT NULL,
  `idPigeon` int(255) NOT NULL,
  `idCat` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `Categorise`
--

INSERT INTO `Categorise` (`idLinkCat`, `idPigeon`, `idCat`) VALUES
(1, 3, 2);

-- --------------------------------------------------------

--
-- Structure de la table `Commentaire`
--

CREATE TABLE `Commentaire` (
  `idCom` int(5) NOT NULL,
  `textCom` text NOT NULL,
  `nbLike` int(255) DEFAULT NULL,
  `idUser` int(5) NOT NULL,
  `idPigeon` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `Pigeon`
--

CREATE TABLE `Pigeon` (
  `idPigeon` int(5) NOT NULL,
  `prenomPigeon` varchar(255) DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `rateWalk` int(1) DEFAULT NULL,
  `rateOriginality` int(1) DEFAULT NULL,
  `rateVibe` int(1) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `urlPhoto` varchar(510) NOT NULL,
  `idUser` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `Pigeon`
--

INSERT INTO `Pigeon` (`idPigeon`, `prenomPigeon`, `color`, `rateWalk`, `rateOriginality`, `rateVibe`, `place`, `urlPhoto`, `idUser`) VALUES
(1, 'René', 'Shiny', 3, 5, 5, 'Noisy-le-Grand', 'https://previews.123rf.com/images/khunaspix/khunaspix1712/khunaspix171200036/92012940-chocko-rouge-pigeon-voyageur-oiseau-isol%C3%A9-fond-blanc.jpg', 1),
(2, 'Alice', 'Dalmatien', 3, 2, 2, 'Crous de l\'ESIEE', 'https://live.staticflickr.com/4043/4683484280_86cc602121_b.jpg', 1),
(3, 'Jesús', 'Multicolore', 5, 5, 5, 'Asian77', 'https://ssaft.com/Blog/dotclear/public/Windows-Live-Writer/painted-pigeons_B6F2/image_5a055dda-507f-4434-a5dd-963964f5492c.png', 1),
(5, 'Adam', 'Classique', 1, 0, 0, 'IMAC Copernic', 'https://d1i4t8bqe7zgj6.cloudfront.net/02-19-2020/t_5e964801929649aa8fad76816dcd8fca_name_20200219_PUTIN_MAGA_pigeons_HANDOUT_still_2.jpg', 1),
(6, 'Paingeon', 'Classique', 4, 5, 4, 'La fabrique Pains et Bricoles', 'https://external-preview.redd.it/tvI_zi5Org9h_5h_e8j0Zlg7m2g6eF8NhLGlfqRzq4I.jpg?auto=webp&s=b1ac1ee1121ea35954cd8aea644695a984d6a0b7', 1),
(7, 'Laurine', 'Rose', 4, 5, 5, 'Machine à café', 'https://i.pinimg.com/originals/02/6e/2f/026e2fca63b03edf9ea9b51f61318100.jpg', 1);

-- --------------------------------------------------------

--
-- Structure de la table `User`
--

CREATE TABLE `User` (
  `idUser` int(5) NOT NULL,
  `pseudo` varchar(12) NOT NULL,
  `password` varchar(255) NOT NULL,
  `bio` text,
  `typeProfilePicture` enum('profile1','profile2','profile3','profile4') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `User`
--

INSERT INTO `User` (`idUser`, `pseudo`, `password`, `bio`, `typeProfilePicture`) VALUES
(1, 'lwiz', '$2b$12$clELeBHEDH.Ua68kiaH.7u8y2e2dmecLJAPbz1lhSX9JNfccyK6L.', 'cc \r\nlol aagga hh', 'profile2');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Categorie`
--
ALTER TABLE `Categorie`
  ADD PRIMARY KEY (`idCat`),
  ADD UNIQUE KEY `Nom` (`nom`);

--
-- Index pour la table `Categorise`
--
ALTER TABLE `Categorise`
  ADD PRIMARY KEY (`idLinkCat`),
  ADD UNIQUE KEY `idPigeon` (`idPigeon`),
  ADD KEY `idCat` (`idCat`);

--
-- Index pour la table `Commentaire`
--
ALTER TABLE `Commentaire`
  ADD PRIMARY KEY (`idCom`),
  ADD KEY `idPigeon` (`idPigeon`),
  ADD KEY `idUser` (`idUser`);

--
-- Index pour la table `Pigeon`
--
ALTER TABLE `Pigeon`
  ADD PRIMARY KEY (`idPigeon`),
  ADD KEY `idProfil` (`idUser`);

--
-- Index pour la table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`idUser`),
  ADD UNIQUE KEY `Pseudo` (`pseudo`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Categorie`
--
ALTER TABLE `Categorie`
  MODIFY `idCat` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `Categorise`
--
ALTER TABLE `Categorise`
  MODIFY `idLinkCat` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `Pigeon`
--
ALTER TABLE `Pigeon`
  MODIFY `idPigeon` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `User`
--
ALTER TABLE `User`
  MODIFY `idUser` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Categorise`
--
ALTER TABLE `Categorise`
  ADD CONSTRAINT `categorise_ibfk_1` FOREIGN KEY (`idCat`) REFERENCES `Categorie` (`idCat`),
  ADD CONSTRAINT `categorise_ibfk_2` FOREIGN KEY (`idPigeon`) REFERENCES `Pigeon` (`idPigeon`);

--
-- Contraintes pour la table `Commentaire`
--
ALTER TABLE `Commentaire`
  ADD CONSTRAINT `commentaire_ibfk_1` FOREIGN KEY (`idPigeon`) REFERENCES `Pigeon` (`idPigeon`),
  ADD CONSTRAINT `commentaire_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `User` (`idUser`);

--
-- Contraintes pour la table `Pigeon`
--
ALTER TABLE `Pigeon`
  ADD CONSTRAINT `pigeon_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`idUser`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
