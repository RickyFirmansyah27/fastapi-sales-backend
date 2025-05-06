from config.db_config import command_with_params
import json

def get_sales_reps(params):
    base_query = """
        SELECT json_agg(sales_rep_data) AS salesReps
        FROM (
            SELECT 
                sr.id,
                sr.name,
                sr.role,
                sr.region,
                COALESCE(json_agg(DISTINCT sk.skill) FILTER (WHERE sk.id IS NOT NULL), '[]') AS skills,
                COALESCE(json_agg(DISTINCT jsonb_build_object(
                    'client', d.client,
                    'value', d.value,
                    'status', d.status
                )) FILTER (WHERE d.id IS NOT NULL), '[]') AS deals,
                COALESCE(json_agg(DISTINCT jsonb_build_object(
                    'name', c.name,
                    'industry', c.industry,
                    'contact', c.contact
                )) FILTER (WHERE c.id IS NOT NULL), '[]') AS clients
            FROM sales_reps sr
            LEFT JOIN skills sk ON sr.id = sk.sales_rep_id
            LEFT JOIN deals d ON sr.id = d.sales_rep_id
            LEFT JOIN clients c ON sr.id = c.sales_rep_id
    """
    count_query = "SELECT COUNT(DISTINCT sr.id) FROM sales_reps sr"
    where_clauses = []
    query_params = []
    
    # Optional filters
    if 'region' in params:
        where_clauses.append("sr.region ILIKE %s")
        query_params.append(f"%{params['region']}%")
    if 'role' in params:
        where_clauses.append("sr.role ILIKE %s")
        query_params.append(f"%{params['role']}%")
    if 'name' in params:
        where_clauses.append("sr.name ILIKE %s")
        query_params.append(f"%{params['name']}%")
    if 'id' in params:
        where_clauses.append("sr.id = %s")
        query_params.append(int(params['id']))

    if 'id' in params:
        where_clauses.append("sr.id = %s")
        query_params.append(int(params['id']))
    
    # Modify email filter to use client's contact field
    if 'email' in params:
        where_clauses.append("EXISTS (SELECT 1 FROM clients c2 WHERE c2.sales_rep_id = sr.id AND c2.contact ILIKE %s)")
        query_params.append(f"%{params['email']}%")
    
    # Add filter for status (assuming it's in deals table)
    if 'status' in params:
        where_clauses.append("EXISTS (SELECT 1 FROM deals d2 WHERE d2.sales_rep_id = sr.id AND d2.status ILIKE %s)")
        query_params.append(f"%{params['status']}%")
    
    # Add filter for amount/value range
    if 'amount' in params:
        where_clauses.append("EXISTS (SELECT 1 FROM deals d3 WHERE d3.sales_rep_id = sr.id AND d3.value = %s)")
        query_params.append(float(params['amount']))

    if where_clauses:
        where_clause = " WHERE " + " AND ".join(where_clauses)
        base_query += where_clause
        count_query += where_clause
        
    base_query += " GROUP BY sr.id, sr.name, sr.role, sr.region"

    sort_by = params.get('sort_by', 'id')
    sort_order = params.get('sort_order', 'ASC')
    allowed_sort_fields = ['id', 'name', 'role', 'region']
    sort_by = sort_by if sort_by in allowed_sort_fields else 'id'
    sort_order = sort_order.upper() if sort_order.upper() in ['ASC', 'DESC'] else 'ASC'
    base_query += f" ORDER BY sr.{sort_by} {sort_order}"
    
    # Closing the subquery
    base_query += ") AS sales_rep_data"
    
    # Pagination
    page = int(params.get('page', 1))
    size = int(params.get('size', 5))
    offset = (page - 1) * size
    base_query += " LIMIT %s OFFSET %s"
    query_params.extend([size, offset])
    
    total_data = command_with_params(count_query, query_params[:len(query_params)-2])[0][0]
    data = command_with_params(base_query, query_params)
    
    sales_reps = []
    if data:
        if isinstance(data[0], dict) and 'salesReps' in data[0]:
            sales_reps = data[0]['salesReps'] or []
        elif len(data) > 0 and isinstance(data[0], tuple) and len(data[0]) > 0:
            if isinstance(data[0][0], dict) and 'salesReps' in data[0][0]:
                sales_reps = data[0][0]['salesReps'] or []
            else:
                sales_reps = data[0][0] if data[0][0] is not None else []
    
    return total_data, sales_reps