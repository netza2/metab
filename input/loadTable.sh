deepdive  sql 'INSERT INTO sentences (SELECT doc_id, sentence_index, to_json(tokens) AS tokens, to_json(lemmas) AS lemmas, to_json(pos_tags) AS pos_tags,to_json(ner_tags) AS ner_tags, to_json(doc_offsets) AS doc_offsets, to_json(dep_types) AS dep_types, to_json(dep_tokens) AS dep_tokens FROM sentences_tsv)'
deepdive compile
