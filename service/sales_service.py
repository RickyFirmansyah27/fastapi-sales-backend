from config.db_query import get_sales_reps
import logging

# Configure logging
logger = logging.getLogger('info')

def getSalesReps(params):
    logger.info(f'[SalesRepsService] - payload: {params}')
    try:
        total_data, sales_reps = get_sales_reps(params)
        
        if not sales_reps:
            return total_data, []
            
        if not isinstance(sales_reps, list):
            sales_reps = [sales_reps]
            
        sales_rep_list = []
        for rep in sales_reps:
            if isinstance(rep, dict):
                rep_dict = {
                    "id": rep.get("id"),
                    "name": rep.get("name"),
                    "role": rep.get("role"),
                    "region": rep.get("region"),
                    "skills": rep.get("skills", []),
                    "deals": rep.get("deals", []),
                    "clients": rep.get("clients", [])
                }
                sales_rep_list.append(rep_dict)
            else:
                logger.warning(f'[SalesRepsService] - Unexpected data type: {type(rep)}. Data: {rep}')
        
        logger.info('[SalesRepsService] - end')
        return total_data, sales_rep_list
    except Exception as err:
        logger.info(f'[SalesRepsService] - error: {err}')
        raise Exception(f"Error fetching sales reps: {str(err)}")
    
