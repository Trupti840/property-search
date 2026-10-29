CREATE TABLE properties (
  id BIGSERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  description TEXT,
  locality VARCHAR NOT NULL,
  city VARCHAR NOT NULL DEFAULT 'Pune',
  bhk INTEGER NOT NULL,
  price BIGINT NOT NULL,
  area_sqft INTEGER,
  parking BOOLEAN NOT NULL DEFAULT FALSE,
  possession_status INTEGER NOT NULL DEFAULT 0,
  amenities JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMP(6) NOT NULL DEFAULT now(),
  updated_at TIMESTAMP(6) NOT NULL DEFAULT now()
);
CREATE INDEX index_properties_on_locality ON properties (locality);
CREATE INDEX index_properties_on_bhk_and_price ON properties (bhk, price);