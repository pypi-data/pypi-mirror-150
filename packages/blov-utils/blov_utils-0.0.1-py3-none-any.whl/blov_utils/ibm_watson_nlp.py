"""
These functions are all about how we leverage IBM Watson to enrich our content
"""
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, KeywordsOptions, ConceptsOptions, EntitiesOptions, SentimentOptions

from Config.settings import ibm_nlp_authenticator_key, ibm_nlp_service_url

authenticator = IAMAuthenticator(ibm_nlp_authenticator_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(ibm_nlp_service_url)

acceptable_entity_types = ['Person', 'Broadcaster', 'Company', 'Facility', 'HealthCondition', 'JobTitle', 'Movie', 'MusicGroup', 'NaturalEvent', 
                            'Organization', 'PrintMedia', 'Sport', 'SportingEvent', 'TelevisionShow', 'Vehicle', 'Award', 'Location']
    
def generate_text_categories(text):
    """
    This function gets the top 5 categories 
    """
    # Make API call to IBM Watson
    response = natural_language_understanding.analyze(
        text= text,
        features=Features(categories=CategoriesOptions(limit=5))).get_result()

    # Process the category response
    article_category_dict = {}
    category_response = response['categories']
    category_tags = []
    
    for cat in category_response:
        conf_score = cat['score']
        category_name = cat['label']
        category_levels = category_name.split('/')
        category_levels = [cat for cat in category_levels if len(cat) > 0]
        category_tags += category_levels

        cat_dict = {
            'Name': category_name,
            'Confidence Score': conf_score
        }
        article_category_dict.update({category_name:cat_dict})
    
    return category_tags, article_category_dict


def generate_text_keywords(text):
    
    response = natural_language_understanding.analyze(
        text= text,
        features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=40))).get_result()

    # Process the keyword response
    keyword_response = response['keywords']
            
    keyword_tags = []
    keywords_dict = {}
    for key in keyword_response:
        keyword = key['text']
        keyword_tags.append(keyword)
        sentiment_label = key['sentiment']['label']
        sentiment_score = key['sentiment']['score']
        relevance_score = key['relevance']
        emotion_score_dict = key['emotion']
        occurence_count = key['count']
        
        curr_dict = {
            'sentiment' : sentiment_label,
            'sentiment_score' : sentiment_score,
            'keyword_relevance_score' : relevance_score, 
            'keyword_emotion_dict' : emotion_score_dict,
            'keyword_occurence' : occurence_count   
        }
        keywords_dict.update({keyword:curr_dict})
        
    return keyword_tags, keywords_dict


def generate_text_concepts(text):

    response = natural_language_understanding.analyze(
        text= text,
        features=Features(concepts=ConceptsOptions(limit=10))).get_result()

    # Process the concept response
    concept_response = response['concepts']
            
    concept_tags = []
    concept_dict = {}
    
    for con in concept_response:
        
        concept_name = con['text']
        
        # Clean up the concept name to generate the key
        name_words = concept_name.split()
        words = [word.replace(".", "") for word in name_words]
        key = ' '.join(words)
        
        relevance_score = con['relevance']
        dbpedia_link = con['dbpedia_resource']
        
        curr_concept = {
            'name' : concept_name,
            'relevance_score' : relevance_score,
            'dbpedia_link' : dbpedia_link
        }
        
        concept_dict.update({key:curr_concept})
        concept_tags.append(concept_name)
    
    return concept_tags, concept_dict


def generate_text_entities(text):
    response = natural_language_understanding.analyze(
        text= text,
        features=Features(entities=EntitiesOptions(sentiment=True,limit=40, emotion=True))).get_result()

    # Process the entity response
    entities_response = response['entities']
            
    entity_tags = []
    entity_dict = {}
    for ent in entities_response:
        entity = ent['text']
        entity_tags.append(entity)
        entity_type = ent['type']
        sentiment_label = ent['sentiment']['label']
        sentiment_score = ent['sentiment']['score']
        relevance_score = ent['relevance']
        confidence_score = ent['confidence']
        occurence_count = ent['count']
        try:
            disambiguation = ent['disambiguation']
        except:
            disambiguation = 'NA'
            
        try:
            dbpedia = ent['dbpedia_resource']
        except:
            dbpedia = 'NA'
            
        curr_dict = {
            'entity_type' : entity_type,
            'entity_subtypes' : disambiguation,
            'sentiment' : sentiment_label,
            'sentiment_score' : sentiment_score,
            'entity_relevance_score' : relevance_score, 
            'entity_confidence_score' : confidence_score,
            'entity_occurence' : occurence_count,
            'dbpedia_resource' : dbpedia
        }
        entity_dict.update({entity:curr_dict})
        
    return entity_tags, entity_dict


def clean_out_ibm_entities_from_keywords(entity_tags, keyword_tags):
    # Clean out entities from the keywords
    entity_tokens = []

    for entity in entity_tags:
        tokens = entity.split()
        entity_tokens += tokens

    cleaned_keyword_tags = []
    for keyword in keyword_tags:

        keyword_tokens = keyword.split()

        word_list = []
        for word in keyword_tokens:
            count = 0
            for word2 in entity_tokens:
                if word2 in word:
                    count += 1
            if count > 0:
                pass
            else:
                word_list.append(word)
        new_keyword = ' '.join(word_list)
        if len(new_keyword) > 0:
            cleaned_keyword_tags.append(new_keyword)
            
    return cleaned_keyword_tags


def generate_text_sentiment(text):
    response = natural_language_understanding.analyze(
        text= text,
        features=Features(sentiment=SentimentOptions())).get_result()

    # Process the sentiment response
    sentiment_response = response['sentiment']
    text_sentiment = sentiment_response['document']['label']
    text_sentiment_score = sentiment_response['document']['score']
    
    return text_sentiment, text_sentiment_score


def get_metadata_for_text(text):
    # Get categories
    category_tags, category_dict = generate_text_categories(text)

    # Get keywords
    keyword_tags, keywords_dict = generate_text_keywords(text)

    # Get Concepts
    concept_tags, concepts_dict = generate_text_concepts(text)

    # Get Entities
    entity_tags, entity_dict = generate_text_entities(text)

    # Get Sentiment
    text_sentiment, text_sentiment_score = generate_text_sentiment(text)

    text_metadata  = {
            'category_tags' : category_tags,
            'category_dict' : category_dict,
            'keyword_tags' : keyword_tags,
            'keyword_dict' : keywords_dict,
            'concept_tags' : concept_tags,
            'concept_dict' : concepts_dict,
            'entity_tags' : entity_tags,
            'entity_dict' : entity_dict,
            'sentiment' : text_sentiment,
            'sentiment_score' : text_sentiment_score,
        }

    return text_metadata


def get_article_text_metadata(article_text): # This will be superceded by what Bruno has done, but we will add an extra field for the top_3_poc_entities
    """
    Get text metadata dict - add the extra field for top_3_poc_entities to what Bruno already had in the analysis service
    """
    ## Get Article categories and process
    category_tags, category_dict = generate_text_categories(article_text)

    ## Get Article keywords and process
    keyword_tags, keyword_dict = generate_text_keywords(article_text)

    ## Get Article concepts and process
    concept_tags, concept_dict = generate_text_concepts(article_text)

    ## Get Article entities and process
    entity_tags, entity_dict = generate_text_entities(article_text)

    ## Get Article sentiment and process
    article_sentiment, article_sentiment_score = generate_text_sentiment(article_text)

    article_top_3_entities = get_article_top_3_entities(entity_dict)

    text_metadata_dict = {
        'category_tags' : category_tags,
        'category_dict' : category_dict,
        'keyword_tags' : keyword_tags,
        'keyword_dict' : keyword_dict,
        'concept_tags' : concept_tags,
        'concept_dict' : concept_dict,
        'entity_tags' : entity_tags,
        'entity_dict' : entity_dict,
        'top_3_article_entities' : article_top_3_entities,
        'article_sentiment' : article_sentiment,
        'article_sentiment_score' : article_sentiment_score,
    }
    
    return text_metadata_dict