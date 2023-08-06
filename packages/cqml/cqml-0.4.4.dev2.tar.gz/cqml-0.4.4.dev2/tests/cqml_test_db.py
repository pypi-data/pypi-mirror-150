# Databricks notebook source
# MAGIC %md
# MAGIC # CQML
# MAGIC ## Compact Query Meta Language
# MAGIC ### Databricks Test Notebook

# COMMAND ----------

!pip install --upgrade pip
#!pip install cqml
!pip --no-cache-dir install git+https://github.com/TheSwanFactory/cqml.git@ymm-6
!pip install cqml==0.4.4.dev2

import cqml

# COMMAND ----------

KEY="cqml_test"
cvm = cqml.load_cqml(KEY,spark, '.')
cvm.debug = True
cvm.run()
print(cvm.sizes)

# COMMAND ----------

K = list(cvm.df.keys())
print(K)
def d(i): return cvm.df[K[i]]
def view(i):
  print(K[i])
  d(i).show()
def values(i, col): return d(i).select(col).distinct().collect()
view(-1)

# COMMAND ----------

cvm.do_save({})
displayHTML(cvm.pkg.html)

# COMMAND ----------
dbutils.notebook.exit(0)
#spark.sql('create database nauto')

# COMMAND ----------

#spark.sql('drop table if exists default.3g_devices_superfleet')
