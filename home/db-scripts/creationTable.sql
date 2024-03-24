
CREATE TABLE Utilisateurs (courriel varchar(100) PRIMARY KEY, uid integer UNIQUE, nom varchar(50),
               age integer, mdp varchar(50), choix bit);

CREATE TABLE Stocks (ticker varchar(5) PRIMARY KEY, nom varchar(50), prix float, capitalisation float,
                     avg200 float, fluctuation float, volume float);

CREATE TABLE sFavoris (courriel varchar(100), ticker varchar(5),
                      FOREIGN KEY sFavoris(courriel) REFERENCES Utilisateurs(courriel), FOREIGN KEY sFavoris(ticker) REFERENCES Stocks(ticker),
                      PRIMARY KEY (courriel, ticker));

CREATE TABLE Compagnie (nomOfficiel varchar(100), ticker varchar(6), secteur varchar(50), description varchar(2000),
                        siteWeb varchar(100), employes integer, FOREIGN KEY Compagnie(ticker) REFERENCES Stocks(ticker),
                        PRIMARY KEY (nomOfficiel));

CREATE TABLE Bilan (cik integer PRIMARY KEY, ticker varchar(5), coutOperation float, coutRD float,
                    coutVente float, revenue float, profit float, FOREIGN KEY Bilan(ticker)  REFERENCES  Stocks(ticker));

CREATE TABLE Nouvelles (nid INT AUTO_INCREMENT PRIMARY KEY, titre varchar(100), auteur varchar(50), image varchar(2000), texte varchar(2000), date DATE);
















