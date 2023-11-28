#!/usr/bin/env python3

import openai
import json
import env

class ai_interface():
	_ai = openai
	_system_prompts = []
	_user_prompts = []

	# Sets the internal fields to values passed in during class
	# instantiation. Defaults to the values defined in ./env.py

	# TODO?: class constructor that takes a file as argument,
	# otherwise uses default values
	def __init__(self, key=env.OPENAI_API_KEY, model=env.MODEL, max_token=env.TOKEN_MAX, ai_temp=env.TEMP):
		self._ai.api_key = key
		self.model = model
		self.max_tokens = max_token
		self.ai_temp = ai_temp

	# Adds a string to the list of strings containing prompts
	# which the model will not respond to. For example, you may
	# want to tell the model that it is a professional Linux
	# administrator with decades of experience without having
	# it output a response
	def add_system_prompt(self, prompt):
		sys = {"role": "system", "content": prompt}
		self._system_prompts.append(sys)

	# Adds a string to the list of strings containing prompts
	# that you do want it to respond to in the final response
	# that it sends back to you.
	# Note: the api returns to you a single response containing
	# the model's responses to all the prompts in this list
	def add_user_prompt(self, prompt):
		use = {"role": "user", "content": prompt}
		self._user_prompts.append(use)

	# Performs the actual api request and returns just the
	# part of the response containing the text the model
	# responded with
	def interact(self):
		messages = []
		messages.extend(self._system_prompts)
		messages.extend(self._user_prompts)
		response = self._ai.ChatCompletion.create(model=self.model, max_tokens=self.max_tokens, temperature=self.ai_temp, messages=messages)
		return response['choices'][0]['message']['content']
