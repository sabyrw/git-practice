-- 1. Function to search contacts by pattern
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_search TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.name, c.phone FROM contacts c
    WHERE c.name ILIKE '%' || p_search || '%' 
       OR c.phone ILIKE '%' || p_search || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Function for data pagination
CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.phone FROM contacts c
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;