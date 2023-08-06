# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from xyz_util import modelutils

class Video(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "视频"
        ordering = ('-create_time',)

    name = models.CharField("名称", max_length=256, blank=True, default='')
    source_url = models.URLField('源地址', max_length=256, blank=True, default='')
    play_url = models.URLField('播放地址', max_length=256, blank=True, default='')
    cover = models.URLField('封面', max_length=256, blank=True, default='')
    interval = models.PositiveSmallIntegerField('时长(秒)', blank=True, default=0)
    width = models.PositiveSmallIntegerField('宽度', blank=True, default=0)
    height = models.PositiveSmallIntegerField('高度', blank=True, default=0)
    poses = modelutils.JSONField("姿势数据", blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    is_active = models.BooleanField("有效", blank=False, default=True)

    def __str__(self):
        return self.name
