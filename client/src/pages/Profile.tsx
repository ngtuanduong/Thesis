import { Card, Typography, Descriptions, Spin, Progress, Button, Empty, List, Tag, Row, Col } from 'antd';
import { ReloadOutlined, TrophyOutlined } from '@ant-design/icons';
import { useMe } from '../api/queries/useAuth';
import { useMySkills, useComputeSkills } from '../api/queries/useSkills';

const { Title, Text } = Typography;

function Profile() {
  const { data: user, isLoading } = useMe();
  const { data: skills, isLoading: skillsLoading, refetch: refetchSkills } = useMySkills();
  const computeSkillsMutation = useComputeSkills();

  const handleRefreshSkills = async () => {
    try {
      await computeSkillsMutation.mutateAsync();
      refetchSkills();
    } catch (error) {
      console.error('Failed to refresh skills:', error);
    }
  };

  if (isLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  return (
    <div>
      <Title level={3}>Profile</Title>
      <Card style={{ marginTop: 16 }}>
        <Descriptions column={1} bordered>
          <Descriptions.Item label="Name">{user?.name || 'N/A'}</Descriptions.Item>
          <Descriptions.Item label="Email">{user?.email || 'N/A'}</Descriptions.Item>
          <Descriptions.Item label="Role">{user?.role || 'N/A'}</Descriptions.Item>
        </Descriptions>
      </Card>

      <Card
        title={
          <span>
            <TrophyOutlined style={{ marginRight: 8 }} />
            Skill Profile
          </span>
        }
        extra={
          <Button
            icon={<ReloadOutlined />}
            onClick={handleRefreshSkills}
            loading={computeSkillsMutation.isPending}
            size="small"
          >
            Refresh Skills
          </Button>
        }
        style={{ marginTop: 16 }}
      >
        {skillsLoading ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin />
          </div>
        ) : !skills || skills.length === 0 ? (
          <Empty
            description={
              <span>
                <Text type="secondary">No skills tracked yet.</Text>
                <br />
                <Text type="secondary">Solve problems to build your skill profile!</Text>
              </span>
            }
          />
        ) : (
          <>
            <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
              <Col span={24}>
                <Text type="secondary">
                  Your skills are automatically updated when you solve problems.
                  Skills are scored based on successful submissions.
                </Text>
              </Col>
            </Row>
            <List
              dataSource={skills}
              renderItem={(skill: any) => {
                const percentage = Math.min(Math.round(skill.score * 100), 100);
                const color = percentage >= 80 ? '#52c41a' : percentage >= 50 ? '#1890ff' : '#faad14';

                return (
                  <List.Item>
                    <div style={{ width: '100%' }}>
                      <div style={{ marginBottom: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span>
                          <Tag color={color}>{skill.skillName}</Tag>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            Last updated: {new Date(skill.updatedAt).toLocaleDateString()}
                          </Text>
                        </span>
                        <Text strong>{percentage}%</Text>
                      </div>
                      <Progress
                        percent={percentage}
                        strokeColor={color}
                        showInfo={false}
                      />
                    </div>
                  </List.Item>
                );
              }}
            />
          </>
        )}
      </Card>
    </div>
  );
}

export default Profile;
