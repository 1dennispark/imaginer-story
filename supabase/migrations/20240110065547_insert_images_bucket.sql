insert into storage.buckets
  (id, name, public)
values
  ('images', 'images', true);

CREATE POLICY "images bucket policy 1ffg0oo_0" ON storage.objects FOR INSERT TO public WITH CHECK (bucket_id = 'images');
CREATE POLICY "images bucket policy 1ffg0oo_1" ON storage.objects FOR UPDATE TO public USING (bucket_id = 'images');
CREATE POLICY "images bucket policy 1ffg0oo_2" ON storage.objects FOR SELECT TO public USING (bucket_id = 'images');
CREATE POLICY "images bucket policy 1ffg0oo_3" ON storage.objects FOR DELETE TO public USING (bucket_id = 'images');