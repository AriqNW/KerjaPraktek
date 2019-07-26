# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DataPing(models.Model):
    id_p = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    bytes = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    ttl = models.CharField(max_length=255, blank=True, null=True)
    id_st = models.ForeignKey('DataSpeedtest', models.DO_NOTHING, db_column='id_st')

    class Meta:
        managed = False
        db_table = 'data_ping'


class DataPingstatistics(models.Model):
    id_ps = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    packetsend = models.CharField(db_column='packetSend', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packetreceived = models.CharField(db_column='packetReceived', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packetloss = models.CharField(db_column='packetLoss', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packetminimum = models.CharField(db_column='packetMinimum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packetmaximum = models.CharField(db_column='packetMaximum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packetaverage = models.CharField(db_column='packetAverage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_st = models.ForeignKey('DataSpeedtest', models.DO_NOTHING, db_column='id_st')

    class Meta:
        managed = False
        db_table = 'data_pingstatistics'


class DataSpeedtest(models.Model):
    id_st = models.AutoField(primary_key=True)
    serverid = models.CharField(db_column='serverId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sponsor = models.CharField(max_length=255, blank=True, null=True)
    servername = models.CharField(db_column='serverName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    distance = models.CharField(max_length=255, blank=True, null=True)
    ping = models.CharField(max_length=255, blank=True, null=True)
    download = models.CharField(max_length=255, blank=True, null=True)
    upload = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_speedtest'
