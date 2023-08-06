def get_sequence(self, seq_name):
    """
input : key or title
output : ((key, title, text, collection, disambiguation, language, author, ...), ...)
"""
    query = f"""
SELECT
{self.tsequence_name}.id_key, {self.tsequence_name}.key_name, {self.tsequence_name}.name,
{self.tsequence_name}.gloria_patri, {self.tsequence_name}.same_page,
{self.tcontent_name}.collection,
{self.tcontent_name}.title, {self.tcontent_name}.text,
{self.tcontent_name}.disambiguation,
{self.tcontent_name}.language, {self.tcontent_name}.author, {self.tcontent_name}.editor
FROM {self.tsequence_name} LEFT JOIN {self.tcontent_name}
ON {self.tsequence_name}.key_name = {self.tcontent_name}.key
WHERE {self.tsequence_name}.sequence_name = ?
ORDER BY {self.tsequence_name}.id_key
"""
    print(query)
    return  self.request_db(query, (seq_name,))
#endDef
