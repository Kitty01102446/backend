-- Phase 4: Location-based store search
-- Adds latitude/longitude to store_address so nearby-store search can run
-- Haversine distance queries. Values are populated automatically via
-- geocoding (services/geocode_service.py) whenever a store address is
-- created or updated -- never entered manually by admins.

ALTER TABLE store_address
  ADD COLUMN latitude DECIMAL(10,7) NULL AFTER street,
  ADD COLUMN longitude DECIMAL(10,7) NULL AFTER latitude,
  ADD INDEX idx_store_address_latlng (latitude, longitude);
