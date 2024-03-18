
CREATE TABLE Utilisateurs (uid integer PRIMARY KEY, nom varchar(50), courriel varchar(100),
               age integer, mdp varchar(50), choix bit);

CREATE TABLE Stocks (ticker varchar(5) PRIMARY KEY, nom varchar(50), prix float, capitalisation float,
                     dividende float, fluctuation float, volume float);

CREATE TABLE sFavoris (uid integer, ticker varchar(5),
                      FOREIGN KEY sFavoris(uid) REFERENCES Utilisateurs(uid), FOREIGN KEY sFavoris(ticker) REFERENCES Stocks(ticker),
                      PRIMARY KEY (uid, ticker));

CREATE TABLE Compagnie (nomOfficiel varchar(100), ticker varchar(5), secteur varchar(50), description varchar(2000),
                        revenueTTM integer, profitTTM integer, FOREIGN KEY Compagnie(ticker) REFERENCES Stocks(ticker),
                        PRIMARY KEY (nomOfficiel));

CREATE TABLE Bilan (cik integer PRIMARY KEY, nomOfficiel varchar(100), coutOperation float, coutRD float,
                    coutVente float, revenue float, profit float, FOREIGN KEY Bilan(nomOfficiel)  REFERENCES  Compagnie(nomOfficiel));

CREATE TABLE Nouvelles (nid INT AUTO_INCREMENT PRIMARY KEY, titre varchar(100), image varchar(2000), texte varchar(2000));


CREATE TABLE nFavoris (uid integer, nid integer,
                      FOREIGN KEY nFavoris(uid) REFERENCES Utilisateurs(uid), FOREIGN KEY Favoris(nid) REFERENCES Nouvelles(nid),
                      PRIMARY KEY (uid, nid));














