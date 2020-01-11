CREATE TABLE IF NOT EXISTS Speeds
(
    dtDateTime Text,
    fDownloadSpeed Real,
    fUploadSpeed Real
);

CREATE INDEX IF NOT EXISTS Speeds_dtDateTime ON Speeds(dtDateTime);