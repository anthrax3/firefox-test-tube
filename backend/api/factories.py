import datetime

import factory
from django.utils import timezone

from . import models


class DataSetFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Long name for experiment %s' % n)
    slug = factory.Sequence(lambda n: 'experiment-%s' % n)
    created_at = factory.Sequence(
        lambda n: timezone.now() - datetime.timedelta(days=n + 7))
    date = factory.Sequence(
        lambda n: timezone.now() + datetime.timedelta(days=n))
    display = True
    enabled = True

    class Meta:
        model = models.DataSet


class MetricFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'cats_a_purring_%s' % n)
    source_name = factory.Sequence(lambda n: 'scalar_cats_a_purring_%s' % n)
    description = factory.Sequence(lambda n: 'Description for metric %s' % n)
    type = factory.Iterator(['BooleanHistogram', 'CountHistogram',
                             'EnumeratedHistogram', 'ExponentialHistogram',
                             'FlagHistogram'])
    units = 'ms'

    class Meta:
        model = models.Metric


class CollectionFactory(factory.django.DjangoModelFactory):
    dataset = factory.SubFactory(DataSetFactory)
    metric = factory.SubFactory(MetricFactory)
    num_observations = 12345
    population = factory.Sequence(lambda n: 'Group %s' % n)
    subgroup = 'All'

    class Meta:
        model = models.Collection


class PointFactory(factory.django.DjangoModelFactory):
    collection = factory.SubFactory(CollectionFactory)
    bucket = factory.Iterator(['1', '10', '100'])
    proportion = factory.Iterator([0.90, 0.07, 0.03])
    count = factory.Iterator([12600, 980, 420])
    rank = factory.Iterator([1, 2, 3])

    class Meta:
        model = models.Point


class StatsFactory(factory.django.DjangoModelFactory):
    dataset = factory.SubFactory(DataSetFactory)
    metric = factory.SubFactory(MetricFactory)
    population = factory.Sequence(lambda n: 'Group %s' % n)
    subgroup = 'All'
    key = factory.Sequence(lambda n: 'key-%s' % n)
    value = factory.Iterator([1, 10, 100, 1000])

    class Meta:
        model = models.Stats
