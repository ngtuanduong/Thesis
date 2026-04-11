import { useState, useRef, useEffect, type KeyboardEvent } from 'react';
import { Button, Input, Spin, Alert, Popconfirm, Avatar, Tooltip } from 'antd';
import {
  RobotOutlined,
  SendOutlined,
  CloseOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import { useMe } from '../../api/queries/useAuth';
import {
  useChatHistory,
  useSendChatMessage,
  useClearChatHistory,
  useChatTokenUsage,
} from '../../api/queries/useChat';
import type { ChatMessageType } from '../../types';
import styles from './ChatBot.module.css';

const SUGGESTIONS = [
  'How do I submit code?',
  'How does adaptive learning work?',
  'Tips for learning programming?',
];

function formatTime(iso: string) {
  return new Date(iso).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
}

function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: user } = useMe();
  const { data: messages = [], isLoading: historyLoading } = useChatHistory();
  const sendMessage = useSendChatMessage();
  const clearHistory = useClearChatHistory();
  const { data: tokenUsage } = useChatTokenUsage();

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, sendMessage.isPending]);

  if (!user) return null;

  const handleSend = (text?: string) => {
    const msg = (text ?? inputValue).trim();
    if (!msg || sendMessage.isPending) return;
    setInputValue('');
    sendMessage.mutate(msg);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isBudgetExceeded =
    tokenUsage && tokenUsage.tokensUsed >= tokenUsage.tokensLimit;

  const errorMessage = sendMessage.error
    ? (sendMessage.error as { response?: { data?: { message?: string } } })
        ?.response?.data?.message ?? 'Failed to send message'
    : null;

  if (!isOpen) {
    return (
      <Tooltip title="Chat with AdaptBot" placement="left">
        <button
          className={styles.fabButton}
          onClick={() => setIsOpen(true)}
          aria-label="Open chatbot"
        >
          <RobotOutlined />
        </button>
      </Tooltip>
    );
  }

  return (
    <div className={styles.chatPanel}>
      {/* Header */}
      <div className={styles.chatHeader}>
        <div className={styles.chatHeaderLeft}>
          <RobotOutlined />
          <span>AdaptBot</span>
          {tokenUsage && (
            <span className={styles.tokenBadge}>
              {tokenUsage.tokensUsed.toLocaleString()} /{' '}
              {tokenUsage.tokensLimit.toLocaleString()}
            </span>
          )}
        </div>
        <div className={styles.chatHeaderRight}>
          <Popconfirm
            title="Clear conversation?"
            description="This will delete all messages."
            onConfirm={() => clearHistory.mutate()}
            okText="Clear"
            cancelText="Cancel"
          >
            <Button
              type="text"
              size="small"
              icon={<DeleteOutlined />}
              disabled={messages.length === 0}
            />
          </Popconfirm>
          <Button
            type="text"
            size="small"
            icon={<CloseOutlined />}
            onClick={() => setIsOpen(false)}
          />
        </div>
      </div>

      {/* Messages */}
      <div className={styles.messagesArea}>
        {historyLoading ? (
          <div style={{ textAlign: 'center', padding: 24 }}>
            <Spin />
          </div>
        ) : messages.length === 0 && !sendMessage.isPending ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyStateIcon}>
              <RobotOutlined />
            </div>
            <div className={styles.emptyStateTitle}>
              Hi! I'm AdaptBot
            </div>
            <div>Ask me about the platform or programming learning.</div>
            <div className={styles.suggestions}>
              {SUGGESTIONS.map((s) => (
                <Button
                  key={s}
                  size="small"
                  block
                  onClick={() => handleSend(s)}
                >
                  {s}
                </Button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg: ChatMessageType) => (
              <div
                key={msg.id}
                className={`${styles.messageRow} ${
                  msg.role === 'user'
                    ? styles.messageRowUser
                    : styles.messageRowAssistant
                }`}
              >
                {msg.role === 'assistant' && (
                  <Avatar
                    size="small"
                    icon={<RobotOutlined />}
                    style={{ flexShrink: 0 }}
                  />
                )}
                <div>
                  <div
                    className={`${styles.messageBubble} ${
                      msg.role === 'user'
                        ? styles.messageBubbleUser
                        : styles.messageBubbleAssistant
                    }`}
                  >
                    {msg.content}
                  </div>
                  <div
                    className={`${styles.messageTime} ${
                      msg.role === 'assistant' ? styles.messageTimeAssistant : ''
                    }`}
                  >
                    {formatTime(msg.createdAt)}
                  </div>
                </div>
              </div>
            ))}
            {sendMessage.isPending && (
              <div className={styles.typingIndicator}>
                <Spin size="small" /> AdaptBot is typing...
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error */}
      {errorMessage && (
        <Alert
          type="warning"
          message={errorMessage}
          closable
          onClose={() => sendMessage.reset()}
          style={{ margin: '0 12px 8px', borderRadius: 6 }}
        />
      )}

      {/* Input */}
      <div className={styles.inputArea}>
        <Input.TextArea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            isBudgetExceeded
              ? 'Daily token limit reached'
              : 'Type a message... (Shift+Enter for newline)'
          }
          maxLength={1000}
          autoSize={{ minRows: 1, maxRows: 3 }}
          disabled={sendMessage.isPending || isBudgetExceeded}
          style={{ flex: 1 }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={() => handleSend()}
          loading={sendMessage.isPending}
          disabled={!inputValue.trim() || isBudgetExceeded}
        />
      </div>
    </div>
  );
}

export default ChatBot;
