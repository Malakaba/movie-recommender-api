

from ga.algorithm import Algorithm
from sqlalchemy.orm import Session
from fastapi import Depends
import numpy as np
import math 

from db.database import get_db
from db.repositories import UserRepository, MovieRepository, RatingsRepository

class MyGeneticAlgorithm(Algorithm):

    def __init__(self, query_search, individual_size, population_size, p_crossover, p_mutation, all_ids, max_generations=100, size_hall_of_fame=1, fitness_weights=(1.0, ), seed=42, db=None) -> None:


        super().__init__(
            individual_size, 
            population_size, 
            p_crossover, 
            p_mutation, 
            all_ids, 
            max_generations, 
            size_hall_of_fame, 
            fitness_weights, 
            seed)
        
        self.db = db
        self.all_ids = all_ids
        self.query_search = query_search
        

    
    def evaluate(self, individual):
        # Verifica se há duplicatas no indivíduo
        if len(individual) != len(set(individual)):
            return (0.0, )
    
        # Verifica se há IDs que não estão na lista de todos os IDs
        if any(id not in self.all_ids for id in individual):
            return (0.0, )
    
        # Obtém as avaliações dos filmes
        ratings_movies = RatingsRepository.find_by_movieid_list(self.db, individual)

        if ratings_movies:
        # Calcula a média das avaliações
            mean_rating = np.mean([obj.rating for obj in ratings_movies])
        else:
            mean_rating = 0.0

        return (mean_rating, )

