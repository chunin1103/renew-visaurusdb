word = "hạnh phúc"  # which means "happiness" in English
synonyms_list = ["niềm vui", "sung sướng", "thỏa mãn", "hài lòng", "phấn khích", "điều tuyệt vời"]

# Example prompt:
print(f"""Examine and refine the following list of potential synonyms for the Vietnamese word \"{word}\": {synonyms_list}. The first priority is to verify and sort the synonyms based on their closeness in meaning to the primary word. Ensure all terms are Vietnamese, including those borrowed from other languages but written in the Latin script. Assess each term's relevance as a synonym, considering their meanings and context-specific usage in Vietnamese. If confident, you may also suggest additional Vietnamese synonyms not listed. Exclude the primary word \"{word}\" itself from the final list. Return the refined list in this format: 'Verified:[comma-separated synonyms]'. If no appropriate Vietnamese synonyms are found, reply with 'Không tìm thấy'.""")
