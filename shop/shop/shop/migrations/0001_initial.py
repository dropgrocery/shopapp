# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shop'
        db.create_table('shop_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('shop', ['Shop'])

        # Adding model 'Taxonomy'
        db.create_table('shop_taxonomy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cat0_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cat1_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cat2_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cat3_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cat4_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('shop', ['Taxonomy'])

        # Adding model 'Product'
        db.create_table('shop_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('taxonomy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Taxonomy'], null=True, blank=True)),
        ))
        db.send_create_signal('shop', ['Product'])

        # Adding model 'ShoppingList'
        db.create_table('shop_shoppinglist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('shoppingdate', self.gf('django.db.models.fields.DateField')()),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Shop'])),
        ))
        db.send_create_signal('shop', ['ShoppingList'])

        # Adding model 'Shoplist_Product'
        db.create_table('shop_shoplist_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('shoplist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.ShoppingList'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('shop', ['Shoplist_Product'])

        # Adding model 'Recipe'
        db.create_table('shop_recipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('instructions', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('shop', ['Recipe'])

        # Adding model 'Recipe_Product'
        db.create_table('shop_recipe_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Recipe'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('shop', ['Recipe_Product'])

        # Adding model 'ProductTag'
        db.create_table('shop_producttag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal('shop', ['ProductTag'])

        # Adding M2M table for field product on 'ProductTag'
        db.create_table('shop_producttag_product', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('producttag', models.ForeignKey(orm['shop.producttag'], null=False)),
            ('product', models.ForeignKey(orm['shop.product'], null=False))
        ))
        db.create_unique('shop_producttag_product', ['producttag_id', 'product_id'])

        # Adding model 'IngredientTag'
        db.create_table('shop_ingredienttag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal('shop', ['IngredientTag'])

        # Adding model 'Ingredient'
        db.create_table('shop_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.IngredientTag'])),
        ))
        db.send_create_signal('shop', ['Ingredient'])


    def backwards(self, orm):
        # Deleting model 'Shop'
        db.delete_table('shop_shop')

        # Deleting model 'Taxonomy'
        db.delete_table('shop_taxonomy')

        # Deleting model 'Product'
        db.delete_table('shop_product')

        # Deleting model 'ShoppingList'
        db.delete_table('shop_shoppinglist')

        # Deleting model 'Shoplist_Product'
        db.delete_table('shop_shoplist_product')

        # Deleting model 'Recipe'
        db.delete_table('shop_recipe')

        # Deleting model 'Recipe_Product'
        db.delete_table('shop_recipe_product')

        # Deleting model 'ProductTag'
        db.delete_table('shop_producttag')

        # Removing M2M table for field product on 'ProductTag'
        db.delete_table('shop_producttag_product')

        # Deleting model 'IngredientTag'
        db.delete_table('shop_ingredienttag')

        # Deleting model 'Ingredient'
        db.delete_table('shop_ingredient')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shop.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.IngredientTag']"})
        },
        'shop.ingredienttag': {
            'Meta': {'object_name': 'IngredientTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'shop.product': {
            'Meta': {'object_name': 'Product'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Taxonomy']", 'null': 'True', 'blank': 'True'})
        },
        'shop.producttag': {
            'Meta': {'object_name': 'ProductTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['shop.Product']", 'symmetrical': 'False'})
        },
        'shop.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'shop.recipe_product': {
            'Meta': {'object_name': 'Recipe_Product'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Product']"}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Recipe']"})
        },
        'shop.shop': {
            'Meta': {'object_name': 'Shop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'shop.shoplist_product': {
            'Meta': {'object_name': 'Shoplist_Product'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Product']"}),
            'shoplist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.ShoppingList']"})
        },
        'shop.shoppinglist': {
            'Meta': {'object_name': 'ShoppingList'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['shop.Product']", 'through': "orm['shop.Shoplist_Product']", 'symmetrical': 'False'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Shop']"}),
            'shoppingdate': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'shop.taxonomy': {
            'Meta': {'object_name': 'Taxonomy'},
            'cat0_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cat1_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cat2_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cat3_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cat4_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['shop']