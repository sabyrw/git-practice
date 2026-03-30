-- 1. Procedure to insert or update a contact (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Procedure to insert multiple contacts with validation
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Simple validation: phone must contain only digits
        IF p_phones[i] ~ '^[0-9]+$' THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            RAISE WARNING 'Invalid phone format for %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Procedure to delete contact by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$;