import { useState, useMemo, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { Typography, Input, Tag, Card, Empty, Select, Space } from 'antd';
import { SearchOutlined, BookOutlined, EnvironmentOutlined, LinkOutlined } from '@ant-design/icons';
import { GLOSSARY, CATEGORY_LABELS } from '../components/onboarding/glossary';
import type { GlossaryEntry, ScaleStop } from '../components/onboarding/glossary';
import { useResponsive } from '../hooks/useResponsive';
import styles from './Glossary.module.css';

const { Title, Text, Paragraph } = Typography;

const CATEGORY_ORDER = ['memory', 'skill', 'system', 'learning'];

/* ── Scale Bar sub-component ── */
function ScaleBar({ stops, unit }: { stops: ScaleStop[]; unit: string }) {
  const gradient = stops
    .map((s) => `${s.color} ${s.value}%`)
    .join(', ');

  const topStops = stops.filter((_, i) => i % 2 === 0);
  const botStops = stops.filter((_, i) => i % 2 !== 0);

  return (
    <div className={styles.scaleContainer}>
      <div className={styles.scaleLabel}>
        Value scale{unit ? ` (${unit})` : ''}
      </div>
      {/* Top row: label above, tick below */}
      <div className={styles.scaleStopsTop}>
        {topStops.map((stop, i) => (
          <div key={i} className={styles.scaleStop} style={{ left: `${stop.value}%` }}>
            <span className={styles.scaleStopLabel}>{stop.label}</span>
            <div className={styles.scaleStopMarker} />
          </div>
        ))}
      </div>
      {/* Gradient bar */}
      <div
        className={styles.scaleBarTrack}
        style={{ background: `linear-gradient(to right, ${gradient})` }}
      />
      {/* Bottom row: tick above, label below */}
      <div className={styles.scaleStopsBot}>
        {botStops.map((stop, i) => (
          <div key={i} className={styles.scaleStop} style={{ left: `${stop.value}%` }}>
            <div className={styles.scaleStopMarker} />
            <span className={styles.scaleStopLabel}>{stop.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── Term Card ── */
function TermCard({
  termKey,
  entry,
  highlighted,
}: {
  termKey: string;
  entry: GlossaryEntry;
  highlighted: boolean;
}) {
  const cat = CATEGORY_LABELS[entry.category] || { label: entry.category, color: '#999' };

  const scrollToTerm = (key: string) => {
    const el = document.getElementById(`term-${key}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <Card
      id={`term-${termKey}`}
      size="small"
      className={`${styles.termCard}${highlighted ? ` ${styles.termCardHighlight}` : ''}`}
      title={
        <Space>
          <Text strong style={{ fontSize: 16, textTransform: 'capitalize' }}>
            {termKey.replace(/_/g, ' ')}
          </Text>
          <Tag color={cat.color}>{cat.label}</Tag>
        </Space>
      }
    >
      <Text strong style={{ fontSize: 14 }}>{entry.short}</Text>
      <Paragraph style={{ marginTop: 8, marginBottom: 0, color: '#595959' }}>
        {entry.detail}
      </Paragraph>

      {/* Scale visualization */}
      {entry.scale && (
        <ScaleBar stops={entry.scale.stops} unit={entry.scale.unit} />
      )}

      {/* Examples */}
      {entry.examples && entry.examples.length > 0 && (
        <div style={{
          background: '#f6f8fa',
          borderRadius: 6,
          padding: '10px 14px',
          borderLeft: `3px solid ${cat.color}`,
          marginTop: 10,
        }}>
          <Text strong style={{ fontSize: 12, color: '#8c8c8c', textTransform: 'uppercase', letterSpacing: 0.5 }}>
            Examples
          </Text>
          <ul style={{ margin: '6px 0 0', paddingLeft: 18 }}>
            {entry.examples.map((ex, i) => (
              <li key={i} style={{ marginBottom: 4, color: '#434343', fontSize: 13 }}>{ex}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Where you see it */}
      {entry.whereYouSeeIt && entry.whereYouSeeIt.length > 0 && (
        <div className={styles.whereSection}>
          <span className={styles.whereSectionLabel}>
            <EnvironmentOutlined style={{ marginRight: 4 }} />
            Where:
          </span>
          {entry.whereYouSeeIt.map((loc, i) => (
            <Tag key={i} className={styles.whereTag} style={{ fontSize: 12 }}>{loc}</Tag>
          ))}
        </div>
      )}

      {/* Related terms */}
      {entry.relatedTerms && entry.relatedTerms.length > 0 && (
        <div className={styles.relatedSection}>
          <span className={styles.relatedSectionLabel}>
            <LinkOutlined style={{ marginRight: 4 }} />
            Related:
          </span>
          {entry.relatedTerms.map((key) => {
            const related = GLOSSARY[key];
            if (!related) return null;
            return (
              <Tag
                key={key}
                color="blue"
                className={styles.relatedTag}
                onClick={() => scrollToTerm(key)}
              >
                {key.replace(/_/g, ' ')}
              </Tag>
            );
          })}
        </div>
      )}
    </Card>
  );
}

/* ── Main Glossary Page ── */
function Glossary() {
  const { isMobile } = useResponsive();
  const location = useLocation();
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [highlightedTerm, setHighlightedTerm] = useState<string | null>(null);
  const didScrollRef = useRef(false);

  const allEntries = useMemo(() =>
    Object.entries(GLOSSARY).map(([key, entry]) => ({ key, entry })),
    [],
  );

  // Deep linking: scroll to term from hash fragment
  useEffect(() => {
    if (didScrollRef.current) return;
    const hash = location.hash.replace('#', '');
    if (!hash || !GLOSSARY[hash]) return;

    didScrollRef.current = true;
    // Small delay to let the DOM render
    const timer = setTimeout(() => {
      const el = document.getElementById(`term-${hash}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setHighlightedTerm(hash);
        setTimeout(() => setHighlightedTerm(null), 2000);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [location.hash]);

  const filtered = useMemo(() => {
    return allEntries.filter(({ key, entry }) => {
      if (categoryFilter !== 'all' && entry.category !== categoryFilter) return false;
      if (!search) return true;
      const q = search.toLowerCase();
      return (
        key.replace(/_/g, ' ').includes(q) ||
        entry.short.toLowerCase().includes(q) ||
        entry.detail.toLowerCase().includes(q) ||
        (entry.examples || []).some((ex) => ex.toLowerCase().includes(q)) ||
        (entry.whereYouSeeIt || []).some((w) => w.toLowerCase().includes(q))
      );
    });
  }, [allEntries, search, categoryFilter]);

  // Group by category
  const groupedByCategory = useMemo(() => {
    const groups: Record<string, { key: string; entry: GlossaryEntry }[]> = {};
    for (const item of filtered) {
      const cat = item.entry.category;
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(item);
    }
    return groups;
  }, [filtered]);

  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const { entry } of allEntries) {
      counts[entry.category] = (counts[entry.category] || 0) + 1;
    }
    return counts;
  }, [allEntries]);

  return (
    <div>
      <div className="responsive-page-header">
        <Title level={3} style={{ margin: 0 }}>
          <BookOutlined style={{ marginRight: 8 }} />
          Terminology Glossary
        </Title>
        <Text type="secondary">{allEntries.length} terms</Text>
      </div>

      {/* Search & Filter */}
      <Space wrap size="middle" style={{ marginTop: 12, width: '100%' }}>
        <Input
          placeholder="Search terms, definitions, examples..."
          prefix={<SearchOutlined />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ width: isMobile ? '100%' : 300 }}
          allowClear
        />
        <Select
          value={categoryFilter}
          onChange={setCategoryFilter}
          style={{ width: 220 }}
          options={[
            { label: `All Categories (${allEntries.length})`, value: 'all' },
            ...CATEGORY_ORDER.map((key) => {
              const meta = CATEGORY_LABELS[key] || { label: key, color: '#999' };
              return {
                label: (
                  <span>
                    <span style={{
                      display: 'inline-block',
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      backgroundColor: meta.color,
                      marginRight: 6,
                    }} />
                    {meta.label} ({categoryCounts[key] || 0})
                  </span>
                ),
                value: key,
              };
            }),
          ]}
        />
      </Space>

      {/* Category-grouped results */}
      <div style={{ marginTop: 24 }}>
        {filtered.length === 0 ? (
          <Empty description="No terms match your search." />
        ) : (
          CATEGORY_ORDER
            .filter((cat) => groupedByCategory[cat]?.length)
            .map((cat) => {
              const meta = CATEGORY_LABELS[cat] || { label: cat, color: '#999' };
              const items = groupedByCategory[cat] || [];
              return (
                <div key={cat} id={`cat-${cat}`} className={styles.categorySection}>
                  <div className={styles.categoryHeader}>
                    <div className={styles.categoryHeaderDot} style={{ backgroundColor: meta.color }} />
                    <Title level={4} style={{ margin: 0 }}>{meta.label}</Title>
                    <Text type="secondary" style={{ marginLeft: 8 }}>
                      {items.length} term{items.length !== 1 ? 's' : ''}
                    </Text>
                  </div>
                  {items.map(({ key, entry }) => (
                    <TermCard
                      key={key}
                      termKey={key}
                      entry={entry}
                      highlighted={highlightedTerm === key}
                    />
                  ))}
                </div>
              );
            })
        )}
      </div>
    </div>
  );
}

export default Glossary;
