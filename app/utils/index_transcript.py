from nlp_utils import extract_entities, nlp, extract_keywords_from_transcript

def index_results_in_elasticsearch():
    for item in results:
        keywords = extract_keywords_from_transcript(item["transcript"])
        doc = VideoDocument(
            title=item["title"],
            url=item["url"],
            transcript=item["transcript"],
            multi_title=keywords
        )
        doc.save()
        print(f"Indexed: {item['title']}")



def index_results_in_elasticsearch():
    for item in results:
        keywords = extract_keywords_from_transcript(item["transcript"])
        doc = VideoDocument(
            title=item["title"],
            url=item["url"],
            transcript=item["transcript"],
            multi_title=keywords
        )
        doc.save()
        print(f"Indexed: {item['title']}")
