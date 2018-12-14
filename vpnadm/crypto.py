from cryptography.hazmat.primitives.hashes import SHA256, SHA512, BLAKE2b
from django.conf import settings
import datetime

DEFAULT_KEY_SIZE  = 4096
DEFAULT_HASH_ALGO = SHA512

def generate_serial():
	from cryptography.x509 import random_serial_number
	return str(random_serial_number())

def generate_default_private_key():
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives.asymmetric import rsa, ec

	return rsa.generate_private_key(
		public_exponent = 65537,
		key_size        = DEFAULT_KEY_SIZE,
		backend = default_backend()
	)

def generate_private_key_pem():
	from cryptography.hazmat.primitives import serialization
	return generate_default_private_key().private_bytes(
		encoding             = serialization.Encoding.PEM,
		format               = serialization.PrivateFormat.PKCS8,
		encryption_algorithm = serialization.NoEncryption()
	).decode('utf-8')
	

def sign_key(client_key_pem, ca_key_pem, ca_crt_pem, cn, serial):
	from cryptography.hazmat.primitives import serialization
	from cryptography.hazmat.primitives.serialization import load_pem_private_key
	from cryptography.hazmat.backends import default_backend
	from cryptography.x509.oid import NameOID
	from cryptography import x509

	client_key = load_pem_private_key(client_key_pem.encode('utf-8'), password = None, backend = default_backend())
	ca_key     = load_pem_private_key(ca_key_pem.encode('utf-8'),     password = None, backend = default_backend())
	ca_crt     = x509.load_pem_x509_certificate(ca_crt_pem.encode('utf-8'), default_backend())

	subject = x509.Name([
		x509.NameAttribute(NameOID.COMMON_NAME,              cn)
	])
	
	cert = x509.CertificateBuilder().subject_name(
		subject
	).issuer_name(
		ca_crt.issuer
	).public_key(
		client_key.public_key()
	).serial_number(
		int(serial)
	).not_valid_before(
		datetime.datetime.utcnow()
	).not_valid_after(
		datetime.datetime.utcnow() + datetime.timedelta(days = settings.CERT_LIFETIME_IN_DAYS)
	).add_extension(
		x509.KeyUsage(
			key_cert_sign      = False,
			crl_sign           = False,
			digital_signature  = True,
			content_commitment = False,
			key_encipherment   = True,
			data_encipherment  = False,
			key_agreement      = False,
			encipher_only      = False,
			decipher_only      = False,
		),
		critical = True,
	).add_extension(
		x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH]),
		critical = True,
	).add_extension(
		x509.SubjectAlternativeName([x509.DNSName(cn)]),
		critical = False,
	).sign(ca_key, DEFAULT_HASH_ALGO(), default_backend())

	cert_pem = cert.public_bytes(encoding = serialization.Encoding.PEM)

	return cert_pem


def generate_ca():
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import serialization
	from cryptography.x509.oid import NameOID
	from cryptography import x509
	
	private_key = generate_default_private_key()
	public_key  = private_key.public_key()
	builder     = x509.CertificateBuilder()

	builder = builder.serial_number(x509.random_serial_number())
	builder = builder.not_valid_before(datetime.datetime.utcnow())
	builder = builder.not_valid_after(
		datetime.datetime.utcnow() + datetime.timedelta(days = settings.CA_LIFETIME_IN_DAYS)
	)
	builder = builder.public_key(public_key)

	name = x509.Name([
		x509.NameAttribute(NameOID.COMMON_NAME,              settings.CA_CN),
		x509.NameAttribute(NameOID.ORGANIZATION_NAME,        settings.CA_O),
		x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, settings.CA_OU),
		x509.NameAttribute(NameOID.LOCALITY_NAME,            settings.CA_L),
		x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,   settings.CA_ST),
		x509.NameAttribute(NameOID.COUNTRY_NAME,             settings.CA_C),
	])
	builder = builder.subject_name(name)
	builder = builder.issuer_name(name)

	builder = builder.add_extension(
		x509.BasicConstraints(ca = True, path_length = None),
		critical = True,
	)

	builder = builder.add_extension(
		x509.KeyUsage(
			key_cert_sign      = True,
			crl_sign           = True,
			digital_signature  = False,
			content_commitment = False,
			key_encipherment   = False,
			data_encipherment  = False,
			key_agreement      = False,
			encipher_only      = False,
			decipher_only      = False,
		),
		critical = True,
	)

	builder = builder.add_extension(
		x509.SubjectKeyIdentifier.from_public_key(public_key),
		critical = False,
	)

	builder = builder.add_extension(
		x509.AuthorityKeyIdentifier.from_issuer_public_key(public_key),
		critical = False,
	)

	cert = builder.sign(
		private_key = private_key,
		algorithm   = DEFAULT_HASH_ALGO(),
		backend     = default_backend()
	)

	private_pem = private_key.private_bytes(
		encoding             = serialization.Encoding.PEM,
		format               = serialization.PrivateFormat.PKCS8,
		encryption_algorithm = serialization.NoEncryption()
	)

	cert_pem = cert.public_bytes(encoding = serialization.Encoding.PEM)

	return cert_pem, private_pem



