# Detection of Energy Consumption Cyber Attacks in IOT devices

RACE M-tech thesis 

# create table
```CREATE TABLE iot_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    device_timestamp BIGINT NOT NULL,
    freeHeapMemory INTEGER NOT NULL,
    networkTrafficVolume INTEGER NOT NULL,
    packetSize INTEGER NOT NULL,
    responseTime INTEGER NOT NULL,
    errorRate FLOAT NOT NULL,
    powerConsumption FLOAT NOT NULL
);
```
# create table Rpi
```
CREATE TABLE rpi_iot_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    devicetimestamp TIMESTAMPTZ NOT NULL,
    cpusage FLOAT NOT NULL,
    freememory FLOAT NOT NULL,
    packetsrecv FLOAT NOT NULL,
    errin FLOAT NOT NULL,
    dropin FLOAT NOT NULL,
    cputemperature FLOAT NOT NULL
);

```