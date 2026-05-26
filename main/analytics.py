from collections import defaultdict
from math import sqrt


BUILDING_RISK = {
    'Permanen': 0.10,
    'Semi Permanen': 0.55,
    'Darurat': 1.00,
    'Sewa/Kontrak': 0.75,
}

DEFAULT_GEREJA_WEIGHTS = {
    'jumlah_umat': 0.30,
    'risiko_bangunan': 0.25,
    'kesenjangan_pelayan': 0.25,
    'tekanan_wilayah': 0.20,
}

DEFAULT_MASJID_WEIGHTS = {
    'kelengkapan_pengurus': 0.35,
    'musholla': 0.25,
    'tekanan_kua': 0.25,
    'kelengkapan_keterangan': 0.15,
}


def as_number(value):
    return value or 0


def normalize_weights(weights):
    total = sum(max(value, 0) for value in weights.values()) or 1
    return {key: max(value, 0) / total for key, value in weights.items()}


def minmax(values):
    minimum = min(values) if values else 0
    maximum = max(values) if values else 0
    if maximum == minimum:
        return [1 if maximum else 0 for _ in values]
    return [(value - minimum) / (maximum - minimum) for value in values]


def topsis(rows, criteria, weights):
    if not rows:
        return []

    normalized_weights = normalize_weights(weights)
    normalized_columns = {
        criterion: minmax([row['criteria'][criterion] for row in rows])
        for criterion in criteria
    }
    weighted_rows = []

    for index, row in enumerate(rows):
        values = {
            criterion: normalized_columns[criterion][index] * normalized_weights[criterion]
            for criterion in criteria
        }
        weighted_rows.append({**row, 'weighted': values})

    ideals = {
        criterion: max(row['weighted'][criterion] for row in weighted_rows)
        for criterion in criteria
    }
    anti_ideals = {
        criterion: min(row['weighted'][criterion] for row in weighted_rows)
        for criterion in criteria
    }

    ranked_rows = []
    for row in weighted_rows:
        positive_distance = sqrt(sum(
            (row['weighted'][criterion] - ideals[criterion]) ** 2
            for criterion in criteria
        ))
        negative_distance = sqrt(sum(
            (row['weighted'][criterion] - anti_ideals[criterion]) ** 2
            for criterion in criteria
        ))
        denominator = positive_distance + negative_distance
        score = negative_distance / denominator if denominator else 0
        ranked_rows.append({
            **row,
            'score': score,
            'score_percent': round(score * 100, 2),
            'priority': priority_label(score),
        })

    return assign_priority_by_rank(sorted(ranked_rows, key=lambda item: item['score'], reverse=True))


def assign_priority_by_rank(items, high_ratio=0.15, medium_ratio=0.35):
    if not items:
        return items

    high_cutoff = max(1, round(len(items) * high_ratio))
    medium_cutoff = max(high_cutoff + 1, round(len(items) * (high_ratio + medium_ratio)))

    for index, item in enumerate(items):
        if index < high_cutoff:
            item['priority'] = 'Tinggi'
        elif index < medium_cutoff:
            item['priority'] = 'Sedang'
        else:
            item['priority'] = 'Rendah'
    return items


def priority_label(score):
    if score >= 0.67:
        return 'Tinggi'
    if score >= 0.34:
        return 'Sedang'
    return 'Rendah'


def euclidean(left, right):
    return sqrt(sum((left[index] - right[index]) ** 2 for index in range(len(left))))


def dbscan(vectors, eps=0.45, min_samples=4):
    labels = [None] * len(vectors)
    cluster_id = 0

    def neighbors(point_index):
        return [
            index for index, vector in enumerate(vectors)
            if euclidean(vectors[point_index], vector) <= eps
        ]

    for index in range(len(vectors)):
        if labels[index] is not None:
            continue

        point_neighbors = neighbors(index)
        if len(point_neighbors) < min_samples:
            labels[index] = -1
            continue

        labels[index] = cluster_id
        seeds = [item for item in point_neighbors if item != index]

        while seeds:
            current = seeds.pop(0)
            if labels[current] == -1:
                labels[current] = cluster_id
            if labels[current] is not None:
                continue

            labels[current] = cluster_id
            current_neighbors = neighbors(current)
            if len(current_neighbors) >= min_samples:
                for neighbor in current_neighbors:
                    if labels[neighbor] is None:
                        seeds.append(neighbor)

        cluster_id += 1

    return labels


def cluster_name(label):
    return 'Outlier' if label == -1 else f'Cluster {label + 1}'


def silhouette_score(vectors, labels):
    cluster_labels = sorted({label for label in labels if label != -1})
    if len(cluster_labels) < 2:
        return None

    scores = []
    for index, vector in enumerate(vectors):
        own_label = labels[index]
        if own_label == -1:
            continue

        own_cluster = [
            other_index for other_index, label in enumerate(labels)
            if label == own_label and other_index != index
        ]
        if own_cluster:
            intra_distance = sum(euclidean(vector, vectors[item]) for item in own_cluster) / len(own_cluster)
        else:
            intra_distance = 0

        nearest_distance = None
        for cluster_label in cluster_labels:
            if cluster_label == own_label:
                continue
            other_cluster = [
                other_index for other_index, label in enumerate(labels)
                if label == cluster_label
            ]
            if not other_cluster:
                continue
            distance = sum(euclidean(vector, vectors[item]) for item in other_cluster) / len(other_cluster)
            nearest_distance = distance if nearest_distance is None else min(nearest_distance, distance)

        if nearest_distance is None:
            continue
        denominator = max(intra_distance, nearest_distance)
        scores.append((nearest_distance - intra_distance) / denominator if denominator else 0)

    if not scores:
        return None
    return sum(scores) / len(scores)


def cluster_evaluation(labels, vectors):
    clusters = sorted({label for label in labels if label != -1})
    noise = sum(1 for label in labels if label == -1)
    silhouette = silhouette_score(vectors, labels)
    return {
        'total_data': len(labels),
        'cluster_count': len(clusters),
        'outlier_count': noise,
        'outlier_percent': round((noise / len(labels)) * 100, 2) if labels else 0,
        'silhouette': silhouette,
        'silhouette_label': 'Tidak tersedia' if silhouette is None else f'{silhouette:.3f}',
    }


def gereja_rows(gereja_queryset):
    gereja_list = list(gereja_queryset)
    wilayah_totals = defaultdict(lambda: {'umat': 0, 'gereja': 0})

    for gereja in gereja_list:
        wilayah_totals[gereja.kecamatan]['umat'] += as_number(gereja.jumlah_umat)
        wilayah_totals[gereja.kecamatan]['gereja'] += 1

    rows = []
    for gereja in gereja_list:
        pelayan = as_number(gereja.jumlah_pdt) + as_number(gereja.jumlah_pdm)
        jumlah_umat = as_number(gereja.jumlah_umat)
        wilayah = wilayah_totals[gereja.kecamatan]
        rows.append({
            'id': gereja.pk,
            'nama': gereja.nama_gereja,
            'wilayah': gereja.kecamatan,
            'jenis': 'Gereja',
            'detail': gereja.kelurahan_desa or '-',
            'criteria': {
                'jumlah_umat': jumlah_umat,
                'risiko_bangunan': BUILDING_RISK.get(gereja.status_bangunan, 0.40),
                'kesenjangan_pelayan': jumlah_umat / (pelayan + 1),
                'tekanan_wilayah': wilayah['umat'] / (wilayah['gereja'] or 1),
            },
        })
    return rows


def masjid_rows(masjid_queryset):
    masjid_list = list(masjid_queryset)
    kua_totals = defaultdict(lambda: {'masjid': 0, 'musholla': 0})

    for masjid in masjid_list:
        wilayah = masjid.wilayah_kua or 'Tidak diketahui'
        kua_totals[wilayah]['masjid'] += 1
        if masjid.ada_musholla:
            kua_totals[wilayah]['musholla'] += 1

    rows = []
    for masjid in masjid_list:
        wilayah = masjid.wilayah_kua or 'Tidak diketahui'
        missing_pengurus = int(not masjid.nama_imam) + int(not masjid.ketua_btm)
        rows.append({
            'id': masjid.pk,
            'nama': masjid.nama_masjid or '-',
            'wilayah': wilayah,
            'jenis': 'Masjid',
            'detail': masjid.desa or '-',
            'criteria': {
                'kelengkapan_pengurus': missing_pengurus / 2,
                'musholla': 0 if masjid.ada_musholla else 1,
                'tekanan_kua': kua_totals[wilayah]['masjid'],
                'kelengkapan_keterangan': 0 if masjid.keterangan else 1,
            },
        })
    return rows


def apply_clusters(ranked_rows, criteria, eps=0.45, min_samples=4):
    if not ranked_rows:
        return ranked_rows, [], cluster_evaluation([], [])

    normalized_columns = [
        minmax([row['criteria'][criterion] for row in ranked_rows])
        for criterion in criteria
    ]
    vectors = [
        [column[index] for column in normalized_columns]
        for index in range(len(ranked_rows))
    ]
    labels = dbscan(vectors, eps=eps, min_samples=min_samples)
    cluster_summary = defaultdict(int)

    for row, label in zip(ranked_rows, labels):
        row['cluster_label'] = label
        row['cluster'] = cluster_name(label)
        cluster_summary[row['cluster']] += 1

    return ranked_rows, sorted(cluster_summary.items()), cluster_evaluation(labels, vectors)


def wilayah_summary(ranked_rows):
    wilayah = defaultdict(lambda: {'total': 0, 'score': 0, 'tinggi': 0, 'sedang': 0, 'rendah': 0})
    for row in ranked_rows:
        item = wilayah[row['wilayah']]
        item['total'] += 1
        item['score'] += row['score']
        item[row['priority'].lower()] += 1

    summary = []
    for name, values in wilayah.items():
        average = values['score'] / values['total'] if values['total'] else 0
        summary.append({
            'nama': name,
            'total': values['total'],
            'score': average,
            'score_percent': round(average * 100, 2),
            'priority': priority_label(average),
            'tinggi': values['tinggi'],
            'sedang': values['sedang'],
            'rendah': values['rendah'],
        })
    return assign_priority_by_rank(sorted(summary, key=lambda item: item['score'], reverse=True), high_ratio=0.20, medium_ratio=0.35)


def priority_summary(ranked_rows):
    summary = {'Tinggi': 0, 'Sedang': 0, 'Rendah': 0}
    for row in ranked_rows:
        summary[row['priority']] += 1
    return summary


def cluster_profiles(ranked_rows, criteria):
    clusters = defaultdict(list)
    for row in ranked_rows:
        clusters[row['cluster']].append(row)

    profiles = []
    for label, rows in clusters.items():
        averages = {}
        for criterion in criteria:
            averages[criterion] = sum(row['criteria'][criterion] for row in rows) / len(rows)
        profiles.append({
            'label': label,
            'total': len(rows),
            'avg_score': sum(row['score'] for row in rows) / len(rows),
            'avg_score_percent': round((sum(row['score'] for row in rows) / len(rows)) * 100, 2),
            'priority_summary': priority_summary(rows),
            'averages': averages,
        })
    return sorted(profiles, key=lambda item: item['avg_score'], reverse=True)


def run_spk_gereja(gereja_queryset, eps=0.45, min_samples=4):
    criteria = list(DEFAULT_GEREJA_WEIGHTS.keys())
    ranked = topsis(gereja_rows(gereja_queryset), criteria, DEFAULT_GEREJA_WEIGHTS)
    ranked, clusters, evaluation = apply_clusters(ranked, criteria, eps, min_samples)
    return {
        'ranked': ranked,
        'clusters': clusters,
        'evaluation': evaluation,
        'wilayah': wilayah_summary(ranked),
        'weights': DEFAULT_GEREJA_WEIGHTS,
        'priority_summary': priority_summary(ranked),
        'cluster_profiles': cluster_profiles(ranked, criteria),
        'criteria': criteria,
        'eps': eps,
        'min_samples': min_samples,
    }


def run_spk(gereja_queryset, masjid_queryset, eps=0.45, min_samples=4):
    gereja_criteria = list(DEFAULT_GEREJA_WEIGHTS.keys())
    masjid_criteria = list(DEFAULT_MASJID_WEIGHTS.keys())

    gereja_ranked = topsis(gereja_rows(gereja_queryset), gereja_criteria, DEFAULT_GEREJA_WEIGHTS)
    gereja_ranked, gereja_clusters, gereja_evaluation = apply_clusters(gereja_ranked, gereja_criteria, eps, min_samples)

    masjid_ranked = topsis(masjid_rows(masjid_queryset), masjid_criteria, DEFAULT_MASJID_WEIGHTS)
    masjid_ranked, masjid_clusters, masjid_evaluation = apply_clusters(masjid_ranked, masjid_criteria, eps, min_samples)

    combined = sorted(gereja_ranked + masjid_ranked, key=lambda item: item['score'], reverse=True)
    return {
        'gereja_ranked': gereja_ranked,
        'masjid_ranked': masjid_ranked,
        'combined_ranked': combined,
        'gereja_clusters': gereja_clusters,
        'masjid_clusters': masjid_clusters,
        'gereja_evaluation': gereja_evaluation,
        'masjid_evaluation': masjid_evaluation,
        'gereja_wilayah': wilayah_summary(gereja_ranked),
        'masjid_wilayah': wilayah_summary(masjid_ranked),
        'gereja_weights': DEFAULT_GEREJA_WEIGHTS,
        'masjid_weights': DEFAULT_MASJID_WEIGHTS,
        'eps': eps,
        'min_samples': min_samples,
    }
