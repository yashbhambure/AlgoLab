from backend.app.algorithms.registry import registry

algos = registry.list_all()
print(f'Total registered algorithms: {len(algos)}')
print('\nAll registered algorithm slugs:')
for i, algo in enumerate(sorted(algos, key=lambda x: x.slug), 1):
    print(f'{i}. {algo.slug} | Category: {algo.category} | Name: {algo.name}')
