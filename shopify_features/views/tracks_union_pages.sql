CREATE VIEW tracks_union_pages AS

select * from tracks
union all
select * from pages