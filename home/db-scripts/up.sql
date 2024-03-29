CREATE TABLE Utilisateurs (nom varchar(50), courriel varchar(100) PRIMARY KEY,
               age integer, mdp varchar(50), premium bit);

CREATE TABLE Stocks (ticker varchar(5) PRIMARY KEY, nom varchar(50), prix float, capitalisation float,
                     dividende float, fluctuation float, volume float);

CREATE TABLE Favoris (id integer, ticker varchar(5),
                      FOREIGN KEY Favoris(id) REFERENCES Utilisateurs(courriel), FOREIGN KEY Favoris(ticker) REFERENCES Stocks(ticker),
                      PRIMARY KEY (id, ticker));