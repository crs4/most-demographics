# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime
from utils import make_new_uid
import string


class IdentifierManager(models.Manager):
    def create_by_json(self, identifier_json_data):
        """Create identifier starting from json structured data.

        Args:
            identifier_json_data: dictionary with identifier data

        Returns:
            new Identifier object
        """
        identifier = self.create(**identifier_json_data)
        return identifier


class Identifier(models.Model):
    """Class Identifier

    Attributes:
        type        (django.db.models.CharField):
        domain      (django.db.models.CharField):
        identifier  (django.db.models.CharField):
    """
    MANDATORY_FIELDS = ('identifier',)

    type = models.CharField(_('Type'), max_length=50, null=True, blank=True)
    domain = models.CharField(_('Domain'), max_length=50, null=True, blank=True)
    identifier = models.CharField(_('Identifier'), max_length=50)
    # add customized manager:
    #objects = IdentifierManager()

    class Meta:
        unique_together = ('type', 'domain', 'identifier')
        verbose_name = _('identifier')
        verbose_name_plural = _('identifiers')

    def __unicode__(self):
        """String representation of a identifier

        Returns:
            String representation of identifier
        """
        identifier_string = u'%s' % self.identifier
        if self.domain:
            identifier_string += u'@%s' % self.domain
        if self.type:
            identifier_string = u'[%s] :: ' % self.type + identifier_string
        return identifier_string

    def to_dictionary(self):
        """Serialize identifier data in a dictionary.

        Returns:
            Dictionary containing identifier data.
        """
        identifier_dictionary = {
            'id': u'%s' % self.id,
            'type': u'%s' % self.type if self.type else None,
            'domain': u'%s' % self.domain if self.domain else None,
            'identifier': u'%s' % self.identifier
        }
        return identifier_dictionary


class CityManager(models.Manager):
    def create_by_json(self, city_json_data):
        """Create city starting from json structured data.

        Args:
            city_json_data: dictionary with city data

        Returns:
            new City object
        """
        city = self.create(**city_json_data)
        return city


class City(models.Model):
    """Class City

    Attributes:
        name        (django.db.models.CharField): city's name
        province    (django.db.models.CharField): city's province
        state       (django.db.models.CharField): city's state
        code        (django.db.models.CharField): city's postal code
    """
    MANDATORY_FIELDS = ('name', 'state')

    name = models.CharField(_('Name'), max_length=255)
    province = models.CharField(_('Province'), max_length=2, null=True, blank=True, help_text=_('Use 2 letters format')) # No control on existence of the province
    state = models.CharField(_('State'), max_length=50, help_text=_('Mandatory'))
    code = models.CharField(_('Code'), max_length=5, null=True, blank=True, help_text=_('e.g. C.A.P., ZIP, etc.'))
    # add customized manager:
    #objects = CityManager()

    class Meta:
        unique_together = (('code', 'name', 'province', 'state'), ('code', 'state'))
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __unicode__(self):
        """String representation of a city

        Returns:
            String representation of city
        """
        city_string = u'%s' % self.name
        if self.code:
            city_string = u'%s - ' % self.code + city_string
        if self.province:
            city_string += u' (%s)' % self.province
        if self.state:
            city_string += u' %s' % self.state
        return city_string

    def save(self, *args, **kwargs):
        """Override save method. Before save the patient upperize some info, if necessary
        """
        # TODO verify if it makes sense
        if self.code and not self.code.isdigit():
            return
        if self.name: self.name = string.capwords(self.name, ' ')
        if self.state: self.state = string.capwords(self.state, ' ')
        if self.province: self.province = self.province.upper()
        super(City, self).save(*args, **kwargs)

    def to_dictionary(self):
        """Serialize city data in a dictionary.

        Returns:
            Dictionary containing city data.
        """
        city_dictionary = {
            'id': u'%s' % self.id,
            'name': u'%s' % self.name,
            'province': u'%s' % self.province if self.province else None,
            'state': u'%s' % self.state if self.state else None,
            'code': u'%s' % self.code if self.code else None
        }
        return city_dictionary


class Patient(models.Model):
    """Class Patient

    Attributes:
        uid                     (django.db.models.CharField)                    : autogenerated unique identification number
        account_number          (django.db.models.CharField)                    : patient national identification number
        first_name              (django.db.models.CharField)                    : patient first name
        last_name               (django.db.models.CharField)                    : patient last name
        other_ids               (django.db.models.ManyToManyField :: Identifier): patient alternative identifiers, other than account_number
        gender                  (django.db.models.CharField)                    : patient gender
        birth_date              (django.db.models.DateField)                    : patient birth date
        birth_place             (django.db.models.ForeignKey :: City)           : patient birth city
        address                 (django.db.models.CharField)                    : patient address
        city                    (django.db.models.ForeignKey :: City)           : patient city address
        phone                   (django.db.models.CharField)                    : patient phone number
        mobile                  (django.db.models.CharField)                    : patient mobile phone number
        email                   (django.db.models.EmailField)                   : patient email
        certified_email         (django.db.models.EmailField)                   : patient certified email
        creation_timestamp      (django.db.models.DateTimeField)                : patient creation timestamp
        last_modified_timestamp (django.db.models.DateTimeField)                : patient last modification timestamp
        deactivation_timestamp  (django.db.models.DateTimeField)                : patient deactivation timestamp
        active                  (django.db.models.BooleanField)                 : patient state

    TODO: define an abstract class <Person> and specialise it with <Patient>
    """
    GENDER_CHOICES = (
        ("M", _("Male")),
        ("F", _("Female")),
    )
    MANDATORY_FIELDS = ('first_name', 'last_name', 'gender', 'birth_date', 'birth_place')

    uid = models.CharField(max_length=40, unique=True, default=make_new_uid)
    account_number = models.CharField(_('National Tax Code'), max_length=16, null=True, blank=True, help_text=_('e.g. SSN'))
    first_name = models.CharField(_('First name'), max_length=50)
    last_name = models.CharField(_('Last name'), max_length=50)
    other_ids = models.ManyToManyField('Identifier', related_name='patient_related', null=True, blank=True, verbose_name=_('Other IDs'))
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(_('Birth date'))
    birth_place = models.ForeignKey('City', related_name='born_patient_related', verbose_name=_('Birth place'))
    address = models.CharField(_('Address'), null=True, blank=True, max_length=255)
    city = models.ForeignKey('City', related_name='addressed_patient_related', null=True, blank=True, verbose_name='City')
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True) # TODO: validation rules
    mobile = models.CharField(_('Mobile phone'), max_length=20, null=True, blank=True) # TODO: validation rules
    email = models.EmailField(_('Email'), null=True, blank=True)
    certified_email = models.EmailField(_('Certified email'), null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_modified_timestamp = models.DateTimeField(auto_now=True)
    deactivation_timestamp = models.DateTimeField(null=True, blank=True, default=None)
    active = models.BooleanField(_('Is the patient active?'), default=True)

    class Meta:
        verbose_name = _('patient')
        verbose_name_plural = _('patients')

    def __unicode__(self):
        """String representation of a patient

        Returns:
            String representation of patient
        """
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """Override save method. Before save the patient upperize some info, if necessary
        """
        if self.first_name: self.first_name = self.first_name.upper()
        if self.last_name: self.last_name = self.last_name.upper()
        if self.account_number: self.account_number = self.account_number.upper()
        if self.pk is not None:
            patient = Patient.objects.get(pk=self.pk)
            if patient.active is True and self.active is False:
                self.deactivation_timestamp = datetime.now()
        super(Patient, self).save(*args, **kwargs)

    def get_age(self, at_date=None):
        """Calculate patient age.

        Args:
            at_date: date to calculate age at. Default None, to calculate age now.

        Returns:
                Tuple (years, weeks) representing the age of a patient now if at_date is None, at certain date if at_date argument is passed
        """
        if at_date:
            if isinstance(at_date, date):
                compare_date = at_date
            else:
                return 0, 0
        else:
            compare_date = date.today()
        birthday = self.birth_date.replace(year=compare_date.year)
        if birthday > compare_date:
            years = compare_date.year - self.birth_date.year -1
            delta = compare_date - birthday
            weeks = int((365.25 + delta.days) / 7)
        else:
            years = compare_date.year - self.birth_date.year
            delta = compare_date - birthday
            weeks = int(delta.days/7)
        return years, weeks

    def to_dictionary(self):
        """Serialize patient data in a dictionary.

        Returns:
            Dictionary containing patient data. other_id attribute is a list of dictionaries representation of Identifier.
            birth_place and address are dictionaries representation of City and Address.
        """
        try:
            birth_date = u'%s' % self.birth_date.strftime('%d %b %Y') if self.birth_date else None
        except Exception, e:
            birth_date = u'%s' % datetime.strptime(self.birth_date, '%Y-%m-%d').strftime('%d %b %Y') \
                if self.birth_date else None
        patient_dictionary = {
            'id': u'%s' % self.id,
            'uid': u'%s' % self.uid,
            'account_number': u'%s' % self.account_number if self.account_number else None,
            'first_name': u'%s' % self.first_name,
            'last_name': u'%s' % self.last_name,
            'other_ids': [],
            'gender': u'%s' % self.get_gender_display(),
            'birth_date': birth_date,
            #'birth_date': u'%s' % self.birth_date if self.birth_date else None,
            'birth_place': self.birth_place.to_dictionary() if self.birth_place else None,
            #'birth_place': u'%s' % self.birth_place if self.birth_place else None,
            'address': self.address if self.address else None,
            'city': self.city.to_dictionary() if self.city else None,
            'phone': u'%s' % self.phone if self.phone else None,
            'mobile': u'%s' % self.mobile if self.mobile else None,
            'email': u'%s' % self.email if self.email else None,
            'certified_email': u'%s' % self.certified_email if self.certified_email else None,
            'active': u'%s' % self.active
        }
        other_ids = self.other_ids.all()
        for identifier in other_ids:
            patient_dictionary['other_ids'].append(identifier.to_dictionary())
        return patient_dictionary
