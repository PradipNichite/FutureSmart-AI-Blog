import nest_asyncio
from llama_parse import LlamaParse

def llama_parse_extract(pdf_path):
  nest_asyncio.apply()
  parser = LlamaParse(
  api_key=  # LLAMA_CLOUD_API_KEY : you can get it from website (it is free now)
  result_type="text",  # "markdown" and "text" are available
  )

  data= parser.load_data(pdf_path)
  return data[0].text