#!/usr/bin/env python3

from openai import OpenAI
import json
import env

class ai_interface():

	# Sets the internal fields to values passed in during class
	# instantiation. Defaults to the values defined in env.py
	# TODO?: class constructor that takes a file as argument,
	# otherwise uses default values
	def __init__(self, key=env.OPENAI_API_KEY, model=env.MODEL, max_token=env.TOKEN_MAX, ai_temp=env.TEMP):
		self._ai = OpenAI(api_key=key)
		self.model = model
		self.max_tokens = max_token
		self.ai_temp = ai_temp
		self.system_prompts = []
		self.user_prompts = []

	# Adds a string to the list of strings containing prompts
	# which the model will not respond to. For example, you may
	# want to tell the model that it is a professional Linux
	# administrator with decades of experience without having
	# it output a response
	def add_system_prompt(self, prompt):
		sys = {"role": "system", "content": prompt}
		self.system_prompts.append(sys)

	# Adds a string to the list of strings containing prompts
	# that you do want it to respond to in the final response
	# that it sends back to you.
	# Note: the api returns to you a single response containing
	# the model's responses to all the prompts in this list
	def add_user_prompt(self, prompt):
		use = {"role": "user", "content": prompt}
		self.user_prompts.append(use)

	# Performs the actual api request and returns just the
	# part of the response containing the text the model
	# responded with
	def interact(self):
		messages = []
		messages.extend(self.system_prompts)
		messages.extend(self.user_prompts)
		response = self._ai.chat.completions.create(
				model=self.model,
				messages=messages,
				max_tokens=self.max_tokens,
				temperature=self.ai_temp
		)
		return response.choices[0].message['content']
